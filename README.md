# jee-finetune

Fine-tuning [Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) to solve **IIT JEE Advanced** problems in Physics, Chemistry, and Mathematics with step-by-step chain-of-thought reasoning.

## Results

Evaluated on 200 held-out questions from [JEEBench](https://huggingface.co/datasets/daman1209arora/jeebench). All models use greedy decoding, max 2,048 tokens.

| Subject | Base Qwen3-8B | SFT | Delta |
|---|---|---|---|
| **Overall** | 78/200 (39.0%) | **90/200 (45.0%)** | **+6.0%** |
| Mathematics | 24/66 (36.4%) | **36/66 (54.5%)** | **+18.2%** |
| Chemistry | 32/70 (45.7%) | **35/70 (50.0%)** | **+4.3%** |
| Physics | **22/64 (34.4%)** | 19/64 (29.7%) | -4.7% |

## Models on HuggingFace

| Model | Size | Link |
|---|---|---|
| SFT (bfloat16) | 16.4 GB | [vipsehgal/qwen3-8b-jee-sft](https://huggingface.co/vipsehgal/qwen3-8b-jee-sft) |
| SDPO (bfloat16) | ~15 GB | [vipsehgal/qwen3-8b-jee-sdpo](https://huggingface.co/vipsehgal/qwen3-8b-jee-sdpo) |
| SDPO MLX 4-bit | 4.3 GB | [vipsehgal/qwen3-8b-jee-sdpo-mlx-4bit](https://huggingface.co/vipsehgal/qwen3-8b-jee-sdpo-mlx-4bit) |

## Pipeline

```
Phase 1: Data Collection & Preparation
  Download datasets → Generate CoT solutions (Claude) → Format → Quality check

Phase 2: Supervised Fine-Tuning (SFT)
  QLoRA on Apple M3 Pro (MLX) → Evaluate → Fuse & export to HuggingFace

Phase 3: Self-Distillation Preference Optimization (SDPO)
  Generate rollouts → Judge (rule-based + LLM) → Build DPO pairs → Train on A100

Phase 4: MLX Conversion
  Convert SDPO model → 4-bit quantize → Local inference on Apple Silicon
```

### Training Data

14,175 examples (12,757 train / 1,418 validation) from:
- **JEEBench CoT** — 457 JEE Advanced questions with Claude-generated step-by-step solutions
- **NuminaMath-CoT** — 2,706 filtered competition math problems (AMC, AIME, Olympiad)
- **PhysReason, PhysicsEval, SciBench** — Physics problem sets
- **ChemistryQA, NCERT, entrance exams** — Chemistry and general science
- **Opus-generated solutions** — 2,337 additional CoT solutions via Claude Sonnet

### SFT Training (Phase 2)

| Parameter | Value |
|---|---|
| Framework | [MLX](https://github.com/ml-explore/mlx-lm) on Apple M3 Pro |
| Method | QLoRA (4-bit base + LoRA adapters) |
| LoRA | rank=8, scale=20, 8 top layers |
| Learning rate | 1e-5 |
| Iterations | 3,500 |
| Effective batch size | 4 (batch=1, grad_accum=4) |
| Max sequence length | 2,048 |
| Training time | ~6-8 hours |

### SDPO Training (Phase 3)

| Parameter | Value |
|---|---|
| Framework | [TRL](https://github.com/huggingface/trl) DPOTrainer on A100 (Colab Pro+) |
| Rollouts | 500 prompts x 2 rollouts |
| DPO beta | 0.1 |
| LoRA | rank=16, alpha=32, all projection layers |
| Learning rate | 5e-6 |
| Epochs | 2 |
| Optimizer | Paged AdamW 8-bit |

## Quick Start

### Inference with MLX (Apple Silicon)

```bash
pip install mlx-lm

# SFT model (recommended)
mlx_lm.generate \
    --model vipsehgal/qwen3-8b-jee-sft \
    --prompt "Solve: Find the number of real solutions of x^3 - 3x + 1 = 0"
```

### Inference with Transformers

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    "vipsehgal/qwen3-8b-jee-sft", torch_dtype="auto", device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("vipsehgal/qwen3-8b-jee-sft")

messages = [
    {"role": "system", "content": "You are an expert IIT JEE tutor. Solve problems step-by-step using LaTeX notation. Show all work clearly and arrive at the final answer."},
    {"role": "user", "content": "A particle of mass 2 kg is projected vertically upward with velocity 20 m/s. Find the maximum height reached. (Take g = 10 m/s^2)"}
]

text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(text, return_tensors="pt").to(model.device)
output = model.generate(**inputs, max_new_tokens=1024)
print(tokenizer.decode(output[0], skip_special_tokens=True))
```

## Reproduce

```bash
# Clone
git clone https://github.com/sehgal-vip/jee-finetune.git
cd jee-finetune

# Install dependencies
pip install -r requirements-mac.txt

# Phase 1: Prepare data (requires ANTHROPIC_API_KEY for CoT generation)
bash run.sh phase1

# Phase 2: SFT training on Mac (6-8 hours)
bash run.sh phase2

# Evaluate
bash run.sh eval-sft

# Phase 3: SDPO on cloud GPU — open colab_phase3_sdpo.ipynb in Google Colab
```

## Project Structure

```
jee-finetune/
  scripts/                     # Data pipeline scripts
    download_datasets.py       #   Dataset downloader
    generate_cot_solutions.py  #   Claude CoT generation
    generate_opus_solutions.py #   Claude Sonnet solutions
    format_data.py             #   Data formatting (68KB, main pipeline)
    data_quality_check.py      #   Automated quality assessment
    prepare_sdpo_data.py       #   SDPO data preparation
  evaluation/
    evaluate.py                # Evaluation script (200-question JEEBench eval)
    compare.py                 # Side-by-side model comparison
    results_base.json          # Base Qwen3-8B: 78/200 (39.0%)
    results_sft.json           # SFT: 90/200 (45.0%)
    results_sdpo.json          # SDPO: 69/200 (34.5%)
  cloud/
    train_sdpo.py              # Full SDPO training script
    judge.py                   # LLM-as-judge for rollout evaluation
    sdpo_config.yaml           # SDPO configuration
  colab_phase3_sdpo.ipynb      # Colab notebook for SDPO training
  run.sh                       # Master orchestration script
  PROJECT_REPORT.md            # Detailed project report
  test_plan.md                 # SFT v2 test plan
```

## Report

See [PROJECT_REPORT.md](PROJECT_REPORT.md) for the full project report covering both training iterations, data pipeline details, and analysis of results.

## License

Apache 2.0
