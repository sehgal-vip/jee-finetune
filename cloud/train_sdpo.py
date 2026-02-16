#!/usr/bin/env python3
"""
Phase 3e: SDPO Training Runner for Cloud GPU.

Integrates the LLM-as-judge verifier with the SDPO training loop.
This script:
  1. Loads the SFT model and SDPO config
  2. Runs RL rollouts on JEE questions
  3. Uses the judge to provide rich feedback
  4. Trains using SDPO (self-distillation from preference optimization)

Run on a cloud GPU with >= 40GB VRAM.
Requires: ANTHROPIC_API_KEY environment variable for the judge.
"""

import json
import os
import sys
import time
from pathlib import Path

import anthropic
import torch
import yaml
from datasets import Dataset
from peft import LoraConfig, get_peft_model
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

from judge import batch_judge, init_cache, get_judge_feedback

SYSTEM_MESSAGE = (
    "You are an expert IIT JEE tutor. Solve problems step-by-step using LaTeX notation. "
    "Show all work clearly and arrive at the final answer."
)


def load_config(config_path: str = "sdpo_config.yaml") -> dict:
    """Load SDPO configuration."""
    with open(config_path) as f:
        return yaml.safe_load(f)


def load_prompts(path: str) -> list[dict]:
    """Load RL prompts from JSONL."""
    prompts = []
    with open(path) as f:
        for line in f:
            if line.strip():
                prompts.append(json.loads(line))
    return prompts


def setup_model(config: dict):
    """Load model and tokenizer with LoRA."""
    model_path = config["model"]["path"]
    dtype = getattr(torch, config["model"].get("dtype", "bfloat16"))

    print(f"Loading model from {model_path}...")
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=dtype,
        device_map="auto",
        trust_remote_code=True,
    )

    # Apply LoRA
    train_cfg = config["training"]
    if train_cfg.get("use_lora", True):
        lora_config = LoraConfig(
            r=train_cfg.get("lora_r", 16),
            lora_alpha=train_cfg.get("lora_alpha", 32),
            lora_dropout=train_cfg.get("lora_dropout", 0.05),
            target_modules=train_cfg.get("lora_target_modules", [
                "q_proj", "k_proj", "v_proj", "o_proj",
                "gate_proj", "up_proj", "down_proj",
            ]),
            task_type="CAUSAL_LM",
        )
        model = get_peft_model(model, lora_config)
        model.print_trainable_parameters()

    return model, tokenizer


def generate_rollouts(
    model,
    tokenizer,
    prompts: list[dict],
    config: dict,
    batch_size: int = 4,
) -> list[dict]:
    """Generate solution attempts for a batch of prompts."""
    rollout_cfg = config.get("rollout", {})
    num_rollouts = rollout_cfg.get("num_rollouts", 4)
    temperature = rollout_cfg.get("temperature", 0.7)
    top_p = rollout_cfg.get("top_p", 0.95)
    max_new_tokens = rollout_cfg.get("max_new_tokens", 1024)

    all_rollouts = []

    for prompt_data in tqdm(prompts, desc="Generating rollouts"):
        question = prompt_data["prompt"]
        ground_truth = prompt_data["ground_truth"]

        # Format as chat
        messages = [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": question},
        ]

        input_text = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = tokenizer(input_text, return_tensors="pt").to(model.device)

        # Generate multiple rollouts
        for _ in range(num_rollouts):
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    do_sample=True,
                    pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
                )

            generated = tokenizer.decode(
                outputs[0][inputs["input_ids"].shape[1]:],
                skip_special_tokens=True,
            )

            all_rollouts.append({
                "question": question,
                "ground_truth": ground_truth,
                "model_output": generated,
                "subject": prompt_data.get("subject", "Unknown"),
                "input_ids": inputs["input_ids"],
            })

    return all_rollouts


def compute_sdpo_loss(
    model,
    teacher_model,
    tokenizer,
    rollout: dict,
    feedback: dict,
    config: dict,
) -> torch.Tensor:
    """Compute SDPO loss for a single rollout.

    SDPO combines:
    1. Standard policy gradient (reward signal from correctness)
    2. Self-distillation from the EMA teacher
    3. Rich feedback distillation (tokenized judge feedback)
    """
    sdpo_cfg = config.get("sdpo", {})
    alpha = sdpo_cfg.get("alpha", 0.5)
    topk = sdpo_cfg.get("distillation_topk", 100)

    # Reward: +1 for correct, -1 for incorrect (with feedback weight)
    reward = 1.0 if feedback["is_correct"] else -0.5

    # Encode the full sequence (question + response)
    messages = [
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": rollout["question"]},
        {"role": "assistant", "content": rollout["model_output"]},
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False)
    tokens = tokenizer(text, return_tensors="pt", truncation=True, max_length=2048).to(model.device)

    # Student logits
    student_outputs = model(**tokens)
    student_logits = student_outputs.logits

    # Teacher logits (no grad)
    with torch.no_grad():
        teacher_outputs = teacher_model(**tokens)
        teacher_logits = teacher_outputs.logits

    # Standard cross-entropy loss on the response portion
    shift_logits = student_logits[..., :-1, :].contiguous()
    shift_labels = tokens["input_ids"][..., 1:].contiguous()
    ce_loss = torch.nn.functional.cross_entropy(
        shift_logits.view(-1, shift_logits.size(-1)),
        shift_labels.view(-1),
        reduction="mean",
    )

    # JSD between student and teacher (top-k for memory efficiency)
    student_probs = torch.nn.functional.softmax(student_logits[..., :-1, :], dim=-1)
    teacher_probs = torch.nn.functional.softmax(teacher_logits[..., :-1, :], dim=-1)

    # Top-k filtering
    if topk > 0 and topk < student_probs.size(-1):
        topk_vals, topk_idx = torch.topk(teacher_probs, topk, dim=-1)
        student_topk = torch.gather(student_probs, -1, topk_idx)
        teacher_topk = topk_vals

        # Renormalize
        student_topk = student_topk / student_topk.sum(dim=-1, keepdim=True).clamp(min=1e-8)
        teacher_topk = teacher_topk / teacher_topk.sum(dim=-1, keepdim=True).clamp(min=1e-8)
    else:
        student_topk = student_probs
        teacher_topk = teacher_probs

    # JSD = alpha * KL(student || M) + (1-alpha) * KL(teacher || M)
    # where M = alpha * student + (1-alpha) * teacher
    M = alpha * student_topk + (1 - alpha) * teacher_topk
    kl_student = torch.nn.functional.kl_div(
        M.log(), student_topk, reduction="batchmean", log_target=False
    )
    kl_teacher = torch.nn.functional.kl_div(
        M.log(), teacher_topk, reduction="batchmean", log_target=False
    )
    jsd_loss = alpha * kl_student + (1 - alpha) * kl_teacher

    # Feedback-weighted loss: richer feedback for wrong answers
    # Encode the feedback and compute a soft loss on it
    feedback_text = feedback["feedback"]
    if not feedback["is_correct"] and feedback_text:
        # Create a training signal from the feedback
        feedback_messages = [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": rollout["question"]},
            {"role": "assistant", "content": feedback_text},
        ]
        fb_text = tokenizer.apply_chat_template(feedback_messages, tokenize=False)
        fb_tokens = tokenizer(fb_text, return_tensors="pt", truncation=True, max_length=2048).to(model.device)

        fb_outputs = model(**fb_tokens)
        fb_logits = fb_outputs.logits
        fb_shift_logits = fb_logits[..., :-1, :].contiguous()
        fb_shift_labels = fb_tokens["input_ids"][..., 1:].contiguous()
        feedback_loss = torch.nn.functional.cross_entropy(
            fb_shift_logits.view(-1, fb_shift_logits.size(-1)),
            fb_shift_labels.view(-1),
            reduction="mean",
        )
    else:
        feedback_loss = torch.tensor(0.0, device=model.device)

    # Combined SDPO loss
    total_loss = reward * ce_loss + jsd_loss + 0.3 * feedback_loss

    return total_loss


def update_ema_teacher(teacher_model, student_model, update_rate: float = 0.05):
    """Update teacher model via exponential moving average."""
    with torch.no_grad():
        for teacher_param, student_param in zip(
            teacher_model.parameters(), student_model.parameters()
        ):
            teacher_param.data.mul_(1 - update_rate).add_(
                student_param.data, alpha=update_rate
            )


def main():
    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Warning: ANTHROPIC_API_KEY not set. Judge will use fallback mode.")

    # Load config
    config = load_config()
    print("SDPO Configuration loaded")

    # Initialize judge cache
    init_cache(config.get("judge", {}).get("cache_path", "judge_cache.jsonl"))

    # Load prompts
    rl_prompts = load_prompts(config["data"]["rl_prompts"])
    eval_prompts = load_prompts(config["data"]["eval_prompts"])
    print(f"Loaded {len(rl_prompts)} RL prompts, {len(eval_prompts)} eval prompts")

    # Load judge config
    judge_config_path = config["data"]["judge_config"]
    judge_config = {}
    if os.path.exists(judge_config_path):
        with open(judge_config_path) as f:
            judge_config = json.load(f)

    # Setup model
    model, tokenizer = setup_model(config)

    # Create EMA teacher (deep copy)
    import copy
    teacher_model = copy.deepcopy(model)
    teacher_model.eval()
    for param in teacher_model.parameters():
        param.requires_grad = False

    # Setup optimizer
    train_cfg = config["training"]
    optimizer = torch.optim.AdamW(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=train_cfg.get("learning_rate", 5e-6),
        weight_decay=train_cfg.get("weight_decay", 0.01),
    )

    # Setup API client for judge
    client = anthropic.Anthropic(api_key=api_key) if api_key else None

    # Training loop
    num_epochs = train_cfg.get("num_epochs", 3)
    batch_size = train_cfg.get("batch_size", 8)
    grad_accum = train_cfg.get("gradient_accumulation_steps", 4)
    max_grad_norm = train_cfg.get("max_grad_norm", 1.0)
    ema_rate = config.get("sdpo", {}).get("teacher_update_rate", 0.05)
    save_every = config.get("checkpoint", {}).get("save_every", 50)
    log_every = config.get("logging", {}).get("log_every", 10)

    # Optional wandb logging
    use_wandb = config.get("logging", {}).get("use_wandb", False)
    if use_wandb:
        try:
            import wandb
            wandb.init(
                project=config["logging"].get("project", "jee-sdpo"),
                name=config["logging"].get("run_name", "qwen3-8b-jee-sdpo"),
                config=config,
            )
        except ImportError:
            print("wandb not installed, skipping logging")
            use_wandb = False

    print(f"\nStarting SDPO training: {num_epochs} epochs, {len(rl_prompts)} prompts")
    print(f"Batch size: {batch_size}, Grad accum: {grad_accum}")

    global_step = 0
    total_correct = 0
    total_judged = 0

    for epoch in range(num_epochs):
        print(f"\n{'='*60}")
        print(f"Epoch {epoch + 1}/{num_epochs}")
        print(f"{'='*60}")

        # Shuffle prompts
        import random
        random.shuffle(rl_prompts)

        epoch_loss = 0.0
        epoch_correct = 0
        epoch_total = 0

        for i in range(0, len(rl_prompts), batch_size):
            batch_prompts = rl_prompts[i : i + batch_size]

            # Generate rollouts
            rollouts = generate_rollouts(model, tokenizer, batch_prompts, config)

            # Judge rollouts
            feedbacks = batch_judge(rollouts, client=client, config=judge_config)

            # Compute SDPO loss for each rollout
            batch_loss = torch.tensor(0.0, device=model.device)
            for rollout, feedback in zip(rollouts, feedbacks):
                loss = compute_sdpo_loss(
                    model, teacher_model, tokenizer, rollout, feedback, config
                )
                batch_loss += loss / (len(rollouts) * grad_accum)

                if feedback["is_correct"]:
                    epoch_correct += 1
                epoch_total += 1

            # Backward pass
            batch_loss.backward()

            # Gradient accumulation step
            if (i // batch_size + 1) % grad_accum == 0:
                torch.nn.utils.clip_grad_norm_(
                    model.parameters(), max_grad_norm
                )
                optimizer.step()
                optimizer.zero_grad()

                # Update EMA teacher
                update_ema_teacher(teacher_model, model, ema_rate)

                global_step += 1
                epoch_loss += batch_loss.item()

                # Logging
                if global_step % log_every == 0:
                    accuracy = epoch_correct / max(epoch_total, 1) * 100
                    print(
                        f"  Step {global_step}: loss={batch_loss.item():.4f}, "
                        f"accuracy={accuracy:.1f}% ({epoch_correct}/{epoch_total})"
                    )
                    if use_wandb:
                        wandb.log({
                            "loss": batch_loss.item(),
                            "accuracy": accuracy,
                            "epoch": epoch + 1,
                            "step": global_step,
                        })

                # Save checkpoint
                if global_step % save_every == 0:
                    ckpt_dir = Path(config["checkpoint"]["save_dir"]) / f"step-{global_step}"
                    ckpt_dir.mkdir(parents=True, exist_ok=True)
                    model.save_pretrained(str(ckpt_dir))
                    tokenizer.save_pretrained(str(ckpt_dir))
                    print(f"  Saved checkpoint to {ckpt_dir}")

        # Epoch summary
        accuracy = epoch_correct / max(epoch_total, 1) * 100
        print(f"\nEpoch {epoch + 1} complete:")
        print(f"  Accuracy: {accuracy:.1f}% ({epoch_correct}/{epoch_total})")
        print(f"  Avg loss: {epoch_loss / max(global_step, 1):.4f}")

    # Save final model
    output_path = config["output"]["save_path"]
    Path(output_path).mkdir(parents=True, exist_ok=True)
    model.save_pretrained(output_path)
    tokenizer.save_pretrained(output_path)
    print(f"\nFinal model saved to {output_path}")

    # Merge LoRA weights if applicable
    if train_cfg.get("use_lora", True):
        print("Merging LoRA weights...")
        merged_model = model.merge_and_unload()
        merged_path = output_path + "-merged"
        Path(merged_path).mkdir(parents=True, exist_ok=True)
        merged_model.save_pretrained(merged_path)
        tokenizer.save_pretrained(merged_path)
        print(f"Merged model saved to {merged_path}")

    if use_wandb:
        wandb.finish()

    print("\nSDPO training complete!")


if __name__ == "__main__":
    main()
