#!/usr/bin/env python3
"""
Phase 1d: Prepare data for SDPO training.

Creates:
  - RL prompts (questions without solutions) for SDPO rollouts
  - Judge configuration for LLM-as-judge feedback
  - Held-out evaluation set
"""

import json
import random
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SDPO_DIR = DATA_DIR / "sdpo"


def extract_question_only(messages: list[dict]) -> str:
    """Extract just the user question from a chat message list."""
    for msg in messages:
        if msg["role"] == "user":
            return msg["content"]
    return ""


def extract_ground_truth(entry: dict) -> str:
    """Extract the ground truth answer from the full entry."""
    import re

    # Try to get from original data fields (JEEBench uses "gold")
    for key in ["answer", "gold", "correct_answer"]:
        if key in entry and entry[key]:
            return str(entry[key])

    # Try to extract from the assistant's response
    messages = entry.get("messages", [])
    for msg in messages:
        if msg["role"] == "assistant":
            # Look for **Answer:** pattern
            match = re.search(r"\*\*Answer:\*\*\s*(.+?)(?:\n|$)", msg["content"])
            if match:
                return match.group(1).strip()
            # Look for boxed answer (common in NuminaMath)
            match = re.search(r"\\boxed\{(.+?)\}", msg["content"])
            if match:
                return match.group(1).strip()
            # Fallback: last line that looks like an answer
            lines = msg["content"].strip().split("\n")
            for line in reversed(lines):
                line = line.strip()
                if line and len(line) < 100:
                    return line

    return ""


def main():
    print("=" * 60)
    print("Phase 1d: Preparing SDPO training data")
    print("=" * 60)

    SDPO_DIR.mkdir(parents=True, exist_ok=True)

    # Load full training data (with metadata)
    train_full_path = DATA_DIR / "train_full.jsonl"
    if not train_full_path.exists():
        print(f"Error: {train_full_path} not found. Run format_data.py first.")
        return

    entries = []
    with open(train_full_path) as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))

    print(f"Loaded {len(entries)} training entries")

    # 1. Create RL prompts (questions without solutions)
    print("\n[1] Creating RL prompts...")
    rl_prompts = []
    for entry in entries:
        question = extract_question_only(entry["messages"])
        ground_truth = extract_ground_truth(entry)
        if question and ground_truth:
            rl_prompts.append({
                "prompt": question,
                "ground_truth": ground_truth,
                "subject": entry.get("metadata", {}).get("subject", "Unknown"),
                "question_type": entry.get("metadata", {}).get("question_type", ""),
                "source": entry.get("metadata", {}).get("source", "unknown"),
            })

    rl_prompts_path = SDPO_DIR / "rl_prompts.jsonl"
    with open(rl_prompts_path, "w") as f:
        for p in rl_prompts:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    print(f"  Saved {len(rl_prompts)} RL prompts to {rl_prompts_path}")

    # 2. Create held-out evaluation set (use validation data)
    print("\n[2] Creating evaluation set...")
    valid_full_path = DATA_DIR / "valid_full.jsonl"
    eval_entries = []
    if valid_full_path.exists():
        with open(valid_full_path) as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    question = extract_question_only(entry["messages"])
                    ground_truth = extract_ground_truth(entry)
                    if question and ground_truth:
                        eval_entries.append({
                            "prompt": question,
                            "ground_truth": ground_truth,
                            "subject": entry.get("metadata", {}).get("subject", "Unknown"),
                            "reference_solution": next(
                                (m["content"] for m in entry["messages"] if m["role"] == "assistant"),
                                "",
                            ),
                        })

    eval_path = SDPO_DIR / "eval_prompts.jsonl"
    with open(eval_path, "w") as f:
        for e in eval_entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    print(f"  Saved {len(eval_entries)} eval prompts to {eval_path}")

    # 3. Create judge configuration
    print("\n[3] Creating judge configuration...")
    judge_config = {
        "model": "claude-opus-4-6-20250929",
        "max_tokens": 2048,
        "system_prompt": (
            "You are an expert IIT JEE examiner evaluating a student's solution. "
            "Analyze the solution step-by-step. If correct, confirm briefly. "
            "If wrong, identify exactly where the reasoning went wrong, "
            "which concept was misapplied, and what the correct approach should be."
        ),
        "correct_template": (
            "Question: {question}\n"
            "Correct answer: {ground_truth}\n"
            "Student's solution: {model_output}\n\n"
            "The student's answer is correct. Provide brief confirmation of the "
            "correct approach and key concepts used."
        ),
        "incorrect_template": (
            "Question: {question}\n"
            "Correct answer: {ground_truth}\n"
            "Student's solution: {model_output}\n\n"
            "Analyze the student's solution step-by-step. Identify exactly where "
            "the reasoning went wrong, which concept was misapplied, and what "
            "the correct approach should be. Be specific and educational."
        ),
        "numerical_tolerance": 0.01,  # 1% tolerance for numerical answers
    }

    judge_config_path = SDPO_DIR / "judge_config.json"
    with open(judge_config_path, "w") as f:
        json.dump(judge_config, f, indent=2)
    print(f"  Saved judge config to {judge_config_path}")

    # Summary
    subject_dist = {}
    for p in rl_prompts:
        subj = p["subject"]
        subject_dist[subj] = subject_dist.get(subj, 0) + 1

    print("\n" + "=" * 60)
    print("SDPO Data Summary:")
    print(f"  RL prompts: {len(rl_prompts)}")
    print(f"  Eval prompts: {len(eval_entries)}")
    print(f"  Subject distribution:")
    for subj, count in sorted(subject_dist.items()):
        print(f"    {subj}: {count}")
    print(f"  Output directory: {SDPO_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
