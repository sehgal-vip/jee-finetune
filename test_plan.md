# Fine-Tuning Test Plan

## Objective
Retrain Qwen3-8B SFT on Phase 2-corrected training data (14,175 examples) and evaluate improvement over the previous run.

## Previous Baseline
- **Model:** Qwen/Qwen3-8B-MLX-4bit + QLoRA adapters (2000 iters on corrupted data)
- **Overall accuracy:** 85/200 (42.5%)
  - Mathematics: 31/66 (47.0%)
  - Physics: 16/64 (25.0%)
  - Chemistry: 38/70 (54.3%)
- **Known data issues (now fixed):**
  - PhysReason: only 128/1200 entries used (dict parsing bug dropped 23.4% of physics data)
  - PhysicsEval: verbose solutions (~11,500 chars median) teaching rambling
  - Mojibake: ~15,685 corrupted characters across training data

## Phase 2 Data Fixes Applied
| Fix | Impact |
|-----|--------|
| B1: PhysReason dict handling | 1,200 entries now formatted (was 128) |
| B2: PhysicsEval verbosity cap | Solutions capped at 3,000 chars |
| B3: Mojibake cleaning | 18 character mappings applied |

## Data Quality (post-fix)
- **Total:** 12,757 train / 1,418 valid
- **Quality score:** 97.2% (all categories PASS)
- **Subject balance:** Math 36.8%, Physics 35.7%, Chemistry 27.5%

---

## Step 1: Back Up Previous Adapters
```bash
mv adapters adapters_v1_corrupted
mkdir -p adapters
```

## Step 2: SFT Training
Run QLoRA fine-tuning on corrected data with same hyperparameters:
```bash
bash scripts/train_sft.sh
```

**Config:**
- Model: `Qwen/Qwen3-8B-MLX-4bit` (4-bit, ~4.5GB)
- LoRA: rank=8, 8 layers, scale=20
- Batch: 1 × 4 gradient accumulation = effective batch 4
- Learning rate: 1e-5
- Iterations: 3500
- Max sequence length: 2048
- Gradient checkpointing: enabled
- Checkpoint every 200 steps

**Estimated time:** ~6-8 hours on 18GB M-series Mac

## Step 3: Smoke Test
```bash
bash scripts/test_sft.sh
```
Manually verify:
- Step-by-step reasoning present
- LaTeX formatted correctly
- Answers in `\boxed{}`
- No mojibake or raw JSON in output

## Step 4: Evaluation
```bash
./run.sh eval-sft
```
Run 200-question benchmark. Compare against baseline.

**Target improvements:**
- Physics: 25% → 35%+ (main beneficiary of PhysReason/PhysicsEval fixes)
- Overall: 42.5% → 48%+
- Math/Chemistry: maintain or improve

## Step 5: Results Comparison
```bash
./run.sh compare
```

## Success Criteria
- [ ] Training completes without errors
- [ ] Validation loss decreases monotonically for first 1000 steps
- [ ] Physics accuracy improves by ≥10 percentage points
- [ ] Overall accuracy ≥ 45%
- [ ] No regression in Math or Chemistry accuracy
