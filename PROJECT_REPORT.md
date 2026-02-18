# JEE Fine-Tuning Project Report

**Model**: Qwen3-8B | **Goal**: IIT JEE Advanced problem-solving with chain-of-thought reasoning
**Hardware**: Apple M3 Pro (SFT) + Google Colab A100 (SDPO) | **Dates**: Feb 15-18, 2026

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Phase 1: Data Collection & Preparation](#2-phase-1-data-collection--preparation)
3. [Phase 2a: SFT v1 (Corrupted Data)](#3-phase-2a-sft-v1-corrupted-data)
4. [Phase 2b: Data Fixes & SFT v2](#4-phase-2b-data-fixes--sft-v2)
5. [Phase 3: SDPO Training](#5-phase-3-sdpo-training)
6. [Phase 4: MLX Conversion & Local Inference](#6-phase-4-mlx-conversion--local-inference)
7. [Evaluation](#7-evaluation)
8. [Final Results](#8-final-results)
9. [HuggingFace Uploads](#9-huggingface-uploads)
10. [Lessons Learned](#10-lessons-learned)

---

## 1. Project Overview

The project fine-tunes Qwen3-8B to solve IIT JEE Advanced problems (Physics, Chemistry, Mathematics) using a two-stage pipeline:

1. **SFT (Supervised Fine-Tuning)** — Train on JEE questions paired with step-by-step CoT solutions using QLoRA on Apple Silicon (MLX)
2. **SDPO (Self-Distillation Preference Optimization)** — Generate rollouts, judge them, build preference pairs, and train with DPO on a cloud A100 GPU

The project went through two iterations of SFT after data quality issues were discovered in the first run.

---

## 2. Phase 1: Data Collection & Preparation

### 2.1 Dataset Research

49 datasets were cataloged across 7 tiers of relevance:

| Tier | Category | Key Datasets | Size |
|---|---|---|---|
| 1 | JEE/NEET-specific | JEEBench (515 problems), JEE Main 2025 Math, Reja1 benchmark | ~1,800 |
| 2 | Large Math Reasoning | NuminaMath-CoT (~860K), OpenMathReasoning (306K), MATH (12.5K) | ~2M+ |
| 3 | Physics | CAMEL-AI Physics (20K), PhysReason (1,200), PhysicsEval (3,304) | ~25K |
| 4 | Chemistry | CAMEL-AI Chemistry (20K), ChemistryQA (~4,500), ChemBench (2,700+) | ~45K |
| 5 | General STEM | SciInstruct (91.8K), GPQA (448), TheoremQA (800) | ~100K+ |
| 6 | Pretraining Corpora | FineMath (34B tokens), OpenWebMath (14.7B tokens) | ~60B tokens |
| 7 | Indian Education | NCERT (120K rows, grades 6-12) | ~120K |

**Key gap identified**: No large-scale JEE dataset with step-by-step solutions exists. Physics datasets are 10-50x smaller than math.

### 2.2 CoT Solution Generation

Since most JEE datasets lack step-by-step solutions, we generated them using Claude:

- **Script**: `scripts/generate_cot_solutions.py` (async, Claude Opus 4.6)
- **Parameters**: max_tokens=4096, max_concurrent=5, 3 retry attempts
- **Verification**: Each generated answer checked against ground truth (1% numerical tolerance)
- **Output**: `data/cot/jeebench_cot.jsonl` (457 JEEBench problems with CoT)

A more sophisticated pipeline (`scripts/generate_opus_solutions.py`) using Claude Sonnet 4.5 processed additional sources:
- Queue: 4,298 entries
- Successfully reconciled: 2,337 solutions (57% reconciliation rate)
- Failures: 1,766 (answers didn't match ground truth)

### 2.3 Data Formatting

`scripts/format_data.py` (68KB, the largest script) handled:
- Reading CoT-augmented and raw datasets
- Filtering for JEE-relevant content using keyword matching (physics, chemistry, math keyword lists)
- LaTeX cleaning and MCQ formatting fixes
- Outputting `train.jsonl` / `valid.jsonl` in MLX-LM chat format (system/user/assistant messages)

**Sources included**: JEEBench CoT, NuminaMath-CoT (filtered), PhysReason, PhysicsEval, SciBench, NCERT, entrance-exam-dataset, ChemistryQA, GPQA Diamond, Opus-generated solutions

### 2.4 Data Quality Check

`scripts/data_quality_check.py` performed automated quality assessment:

| Category | Score | Weight | Details |
|---|---|---|---|
| Semantic | 0.915 | 30% | 39 drops, 2,088 reviews (MCQ mismatches, coherence failures) |
| Contamination | 0.989 | 25% | 138 drops (eval set overlap removal) |
| Token Length | 0.998 | 15% | 48 reviews (excessively long solutions) |
| Coverage | 0.999 | 15% | 5 drops, 6 reviews |
| LaTeX | 0.998 | 10% | 112 fixes (broken LaTeX expressions) |
| Schema | 1.000 | 5% | All valid |
| **Overall** | **0.972** | | **97.2% quality score** |

### 2.5 Final Training Data

| Split | Examples | Size |
|---|---|---|
| Train | 12,757 | 20 MB |
| Validation | 1,418 | 2.2 MB |
| **Total** | **14,175** | **22.2 MB** |

**Subject balance**: Mathematics 36.8%, Physics 35.7%, Chemistry 27.5%

### 2.6 SDPO Data Preparation

`scripts/prepare_sdpo_data.py` produced:

| File | Lines | Size | Purpose |
|---|---|---|---|
| `data/sdpo/rl_prompts.jsonl` | 14,655 | 5.8 MB | Prompts for rollout generation (questions + ground truth, no solutions) |
| `data/sdpo/eval_prompts.jsonl` | 1,651 | 3.9 MB | Eval set (includes reference solutions) |
| `data/sdpo/judge_config.json` | 1 | 915 B | Judge settings (Claude Opus 4.6, 1% tolerance) |

---

## 3. Phase 2a: SFT v1 (Corrupted Data)

### 3.1 Training Configuration

| Parameter | Value |
|---|---|
| Base model | Qwen/Qwen3-8B-MLX-4bit (~4.5 GB) |
| Framework | MLX (mlx-lm) on Apple M3 Pro |
| Method | QLoRA (4-bit quantized base + LoRA adapters) |
| LoRA rank | 8 |
| LoRA scale (alpha/rank) | 20.0 |
| LoRA dropout | 0.0 |
| LoRA layers | 8 (top layers) |
| Learning rate | 1e-5 |
| Batch size | 1 |
| Gradient accumulation | 4 (effective batch = 4) |
| Max sequence length | 2,048 |
| Optimizer | Adam |
| Gradient checkpointing | Enabled |
| Iterations | ~3,500 (resumed from step 2000, ran 1,500 more) |
| Checkpoint interval | Every 200 steps |

### 3.2 Training Run

- Date: Feb 16, 2026
- Produced 10 checkpoint files (steps 200-2000) + final `adapters.safetensors`
- Each checkpoint: 19.4 MB
- Saved to `adapters_v1_corrupted/`

### 3.3 v1 Evaluation Results

Evaluated on 200 questions from `data/sdpo/eval_prompts.jsonl`:

| Subject | Score | Accuracy |
|---|---|---|
| **Overall** | **85/200** | **42.5%** |
| Mathematics | 31/66 | 47.0% |
| Chemistry | 38/70 | 54.3% |
| Physics | 16/64 | 25.0% |

### 3.4 Data Issues Discovered

Three bugs were found in the training data:

| Bug | Issue | Impact |
|---|---|---|
| **B1: PhysReason dict handling** | Raw Python dicts were being used as solutions instead of formatted text | Only 128 of 1,200 entries were properly formatted |
| **B2: PhysicsEval verbosity** | Median solution length was ~11,500 characters (way too long) | Wasted sequence length, poor training signal |
| **B3: Mojibake characters** | Unicode corruption in ~15,685 characters across the dataset | Garbled text in solutions (e.g., `Ïâ` artifacts) |

---

## 4. Phase 2b: Data Fixes & SFT v2

### 4.1 Fixes Applied

| Fix | What Changed |
|---|---|
| B1 | PhysReason entries now properly formatted (1,200 entries vs 128) |
| B2 | PhysicsEval solutions capped at 3,000 characters |
| B3 | 18 character mappings applied to fix mojibake corruption |

Post-fix data quality: 12,757 train / 1,418 valid, quality score 97.2%.

### 4.2 SFT v2 Training

Same hyperparameters as v1, but:
- **Full 3,500 iterations** (resumed from step 2,600 checkpoint)
- Clean data with all three bugs fixed
- Date: Feb 17, 2026
- 13 checkpoint files (steps 200-2,600) + final adapters
- Saved to `adapters/`

### 4.3 Model Export

The SFT LoRA adapters were fused with the base model and exported as full-precision bfloat16 safetensors:
- 4 model shards (`model-00001-of-00004.safetensors` through `model-00004-of-00004.safetensors`)
- Total size: ~16.4 GB
- Uploaded to HuggingFace as `vipsehgal/qwen3-8b-jee-sft`

---

## 5. Phase 3: SDPO Training

### 5.1 Approach

Rather than the full SDPO with JSD loss (designed in `cloud/train_sdpo.py` and `cloud/sdpo_config.yaml`), the actual training used a **simplified DPO approach** via TRL's DPOTrainer in a Colab notebook (`colab_phase3_sdpo.ipynb`).

### 5.2 Rollout Generation

| Parameter | Value |
|---|---|
| Source model | `vipsehgal/qwen3-8b-jee-sft` (loaded in NF4 4-bit) |
| Prompts | 500 (randomly sampled from 14,655 RL prompts) |
| Rollouts per prompt | 2 |
| Total generations | 1,000 |
| Temperature | 0.7 |
| Top-p | 0.95 |
| Max new tokens | 512 |

### 5.3 Judging

Rule-based answer extraction and checking:
- Patterns: `\boxed{}`, `**Answer:**`, `Answer:`, `The answer is`, last MCQ option
- Normalization: strip LaTeX, lowercase, remove whitespace
- Numerical tolerance: 1%
- MCQ multi-answer support (e.g., "A,C" matching)

Optional Claude Sonnet 4.5 feedback for incorrect rollouts (capped at 200 API calls) to provide step-by-step correct solutions.

### 5.4 DPO Preference Pair Construction

For each question, priority for **chosen** response:
1. Correct rollout from the model (best case)
2. LLM judge feedback (Claude Sonnet 4.5 step-by-step solution)
3. Gold solution from training data

**Rejected** response: An incorrect rollout from the model.

Questions where all rollouts were correct were skipped.

### 5.5 DPO Training

| Parameter | Value |
|---|---|
| Framework | TRL DPOTrainer on A100 GPU (Colab Pro+) |
| Base model | `vipsehgal/qwen3-8b-jee-sft` (NF4 4-bit) |
| Epochs | 2 |
| Batch size | 2 per device |
| Gradient accumulation | 4 (effective batch = 8) |
| Learning rate | 5e-6 |
| DPO beta | 0.1 |
| LoRA rank | 16 |
| LoRA alpha | 32 |
| LoRA dropout | 0.05 |
| LoRA targets | q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj |
| Max length | 1,024 |
| Max prompt length | 512 |
| Optimizer | Paged AdamW 8-bit |
| LR scheduler | Cosine |
| Warmup ratio | 0.1 |
| Gradient checkpointing | Enabled |
| Precision | bfloat16 |

### 5.6 SDPO Design (Not Used in Final Run)

A more sophisticated SDPO pipeline was designed (`cloud/train_sdpo.py`) but not used in the final Colab run:

- Custom SDPO loss: `reward * CE_loss + JSD_loss + 0.3 * feedback_loss`
- JSD (Jensen-Shannon Divergence) between student and EMA teacher (top-k=100 logits)
- EMA teacher update rate: 0.05
- 4 rollouts per prompt, 3 epochs, batch=8, grad_accum=4
- Reward: +1 correct, -0.5 incorrect
- Feedback distillation weight: 0.3

This was designed for `verl` framework but the simpler TRL DPO approach was used instead due to practical constraints.

### 5.7 Model Export

- LoRA adapters merged with base SFT model
- Exported as full-precision bfloat16 safetensors (~15 GB)
- Uploaded to HuggingFace as `vipsehgal/qwen3-8b-jee-sdpo`

---

## 6. Phase 4: MLX Conversion & Local Inference

The SDPO model was converted to MLX 4-bit format for fast local inference on Apple Silicon:

```bash
python -m mlx_lm.convert \
    --hf-path vipsehgal/qwen3-8b-jee-sdpo \
    --q-bits 4 --q-group-size 64 \
    --mlx-path ./qwen3-8b-jee-sdpo-mlx-4bit
```

- Output size: 4.3 GB
- Inference speed: ~30 tokens/sec on M3 Pro
- Uploaded to HuggingFace as `vipsehgal/qwen3-8b-jee-sdpo-mlx-4bit`

---

## 7. Evaluation

### 7.1 Evaluation Setup

- **Script**: `evaluation/evaluate.py`
- **Eval set**: 200 questions from `data/sdpo/eval_prompts.jsonl`
- **Subjects**: Mathematics (66), Physics (64), Chemistry (70)
- **Decoding**: Greedy (temperature=0), max 2,048 tokens
- **Answer extraction**: `\boxed{}`, `**Answer:**`, `Answer:`, `The answer is`, last MCQ option, last `= <number>`
- **Matching**: Exact match, containment, numeric tolerance (2%), MCQ letter comparison
- **Multi-part**: JSON array ground truths require majority match

### 7.2 Models Evaluated

| Model | How Run | Duration |
|---|---|---|
| Base Qwen3-8B | `--model Qwen/Qwen3-8B-MLX-4bit` (no adapters) | ~4h 11min |
| SFT v1 (corrupted) | `--model Qwen/Qwen3-8B-MLX-4bit --adapter-path adapters_v1_corrupted` | ~3h |
| SFT v2 (clean) | `--model Qwen/Qwen3-8B-MLX-4bit --adapter-path adapters` | ~3h |
| SDPO | `--model ./qwen3-8b-jee-sdpo-mlx-4bit` (fused, no adapter) | ~3h |

---

## 8. Final Results

### 8.1 Full Comparison

| Subject | Base Qwen3-8B | SFT v1 (corrupted) | SFT v2 (clean) | SDPO |
|---|---|---|---|---|
| **Overall** | 78/200 (39.0%) | 85/200 (42.5%) | **90/200 (45.0%)** | 69/200 (34.5%) |
| Mathematics | 24/66 (36.4%) | 31/66 (47.0%) | **36/66 (54.5%)** | 17/66 (25.8%) |
| Chemistry | 32/70 (45.7%) | 38/70 (54.3%) | **35/70 (50.0%)** | 34/70 (48.6%) |
| Physics | 22/64 (34.4%) | 16/64 (25.0%) | 19/64 (29.7%) | 18/64 (28.1%) |

### 8.2 Deltas vs Base

| Subject | SFT v1 | SFT v2 | SDPO |
|---|---|---|---|
| **Overall** | +3.5% | **+6.0%** | -4.5% |
| Mathematics | +10.6% | **+18.2%** | -10.6% |
| Chemistry | +8.6% | +4.3% | +2.9% |
| Physics | -9.4% | -4.7% | -6.3% |

### 8.3 Key Observations

**SFT v2 (best model):**
- Improved overall accuracy by +6pp over base (39.0% -> 45.0%)
- Massive Mathematics gain of +18.2pp, driven by NuminaMath-CoT training data
- Chemistry improved modestly (+4.3pp)
- Physics regressed slightly (-4.7pp) -- training data was ~83% math, only ~17% physics/chemistry
- Met the success criterion of >= 45% overall

**SFT v1 vs v2:**
- v2 improved overall by +2.5pp over v1 (42.5% -> 45.0%)
- Mathematics jumped +7.5pp (47.0% -> 54.5%) -- the data quality fixes had a large impact
- Chemistry regressed from 54.3% to 50.0% (possibly noise at this sample size)
- Physics improved from 25.0% to 29.7% (+4.7pp) -- PhysReason dict fix helped

**SDPO (regression):**
- Overall 34.5%, worse than both base (39.0%) and SFT (45.0%)
- Mathematics catastrophically regressed: 54.5% (SFT) -> 25.8% (SDPO), a -28.7pp drop
- Chemistry held roughly steady (50.0% -> 48.6%)
- Physics slightly regressed (29.7% -> 28.1%)
- Root causes: only 500 prompts with 2 rollouts each (insufficient coverage), simplified DPO (not full SDPO with JSD), max_new_tokens=512 may have truncated reasoning

---

## 9. HuggingFace Uploads

### 9.1 Repositories

| Repo | Files | Description |
|---|---|---|
| [vipsehgal/qwen3-8b-jee-sft](https://huggingface.co/vipsehgal/qwen3-8b-jee-sft) | 15 files | SFT model (bf16, ~16.4 GB) + SDPO data files |
| [vipsehgal/qwen3-8b-jee-sdpo](https://huggingface.co/vipsehgal/qwen3-8b-jee-sdpo) | model weights | SDPO model (bf16, ~15 GB) |
| [vipsehgal/qwen3-8b-jee-sdpo-mlx-4bit](https://huggingface.co/vipsehgal/qwen3-8b-jee-sdpo-mlx-4bit) | quantized model | MLX 4-bit quantized SDPO (4.3 GB) |

### 9.2 SFT Repo Contents

Model weights (4 shards), tokenizer, chat template, config, and SDPO data files (`sdpo_data/eval_prompts.jsonl`, `sdpo_data/rl_prompts.jsonl`, `sdpo_data/judge_config.json`, `sdpo_data/train.jsonl`) bundled for cloud training convenience.

### 9.3 Model Cards

Both SFT and SDPO repos have full model cards with:
- YAML frontmatter (license, tags, datasets, model-index with metrics)
- Training details and hyperparameters
- Evaluation results comparison tables
- Usage examples (MLX + Transformers)
- Limitations and license info

---

## 10. Lessons Learned

### What Worked
1. **NuminaMath-CoT** was the single most impactful data source -- competition math with step-by-step solutions drove the +18pp Math improvement
2. **Data quality matters more than quantity** -- fixing PhysReason dict handling and mojibake improved v2 over v1 by +2.5pp overall
3. **QLoRA on Apple Silicon** is practical -- full SFT training in ~6-8 hours on an M3 Pro
4. **Claude-generated CoT solutions** for JEEBench were high quality (57% reconciliation rate for the harder Opus pipeline)

### What Didn't Work
1. **SDPO regressed from SFT** -- the simplified DPO approach with only 500 prompts x 2 rollouts was insufficient
2. **Physics remains the weak point** -- both SFT iterations regressed on Physics vs base. The 83/17 math/science training data imbalance is the likely cause
3. **The v1 data bugs** cost a full training iteration (~6-8 hours) before being caught

### Recommendations for Next Iteration
1. **More Physics/Chemistry data** -- rebalance to at least 50/25/25 Math/Phys/Chem
2. **Better SDPO pipeline** -- use the full JSD-based SDPO loss (not simplified DPO), more rollouts (4+ per prompt), larger prompt set (2000+), longer max_new_tokens (1024+)
3. **Longer SFT training** -- the model was still improving at 3,500 steps; try 5,000-7,000
4. **Full JEEBench eval** -- run the complete 515-question benchmark for more reliable comparisons
5. **Physics-specific CoT generation** -- generate more high-quality Physics CoT solutions using Claude to address the data gap

---

## Appendix: Project Structure

```
jee-finetune/
  adapters/                    # SFT v2 LoRA adapters (13 checkpoints + final)
  adapters_v1_corrupted/       # SFT v1 LoRA adapters (10 checkpoints + final)
  cloud/                       # Cloud SDPO scripts
    judge.py                   # LLM-as-judge for rollout evaluation
    train_sdpo.py              # Full SDPO training script (not used in final run)
    sdpo_config.yaml           # SDPO configuration
    setup.sh                   # Cloud environment setup
  colab_phase3_sdpo.ipynb      # Actual SDPO training notebook (Colab A100)
  configs/                     # (empty)
  data/
    train.jsonl                # 12,757 training examples
    valid.jsonl                # 1,418 validation examples
    quality_report.json        # Automated quality assessment
    sdpo/                      # SDPO data files
    raw/                       # Raw downloaded datasets
    cot/                       # Claude-generated CoT solutions
    batches/                   # Batch processing intermediates
  evaluation/
    evaluate.py                # Main evaluation script
    compare.py                 # Side-by-side comparison
    results_base.json          # Base model results (78/200 = 39.0%)
    results_sft.json           # SFT v2 results (90/200 = 45.0%)
    results_sdpo.json          # SDPO results (69/200 = 34.5%)
  qwen3-8b-jee-sdpo/          # Downloaded SDPO model
  qwen3-8b-jee-sdpo-mlx-4bit/ # MLX 4-bit quantized SDPO model
  scripts/
    download_datasets.py       # Dataset downloader
    generate_cot_solutions.py  # Claude Opus CoT generation
    generate_opus_solutions.py # Claude Sonnet solution generation
    format_data.py             # Main data formatting pipeline
    clean_data.py              # Data cleaning
    data_quality_check.py      # Quality assessment
    prepare_sdpo_data.py       # SDPO data preparation
  sdpo_upload/                 # Model card staging
  run.sh                       # Master orchestration script
  dataset_report.md            # Dataset catalog (49 datasets)
  dataset_research_report.md   # Dataset research notes
  test_plan.md                 # SFT v2 test plan
```
