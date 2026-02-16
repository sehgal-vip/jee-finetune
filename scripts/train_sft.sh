#!/usr/bin/env bash
# Phase 2b: Run QLoRA SFT fine-tuning on Mac with MLX
#
# Prerequisites:
#   pip install "mlx-lm[train]"
#   Verify: python -c "import mlx_lm; print(mlx_lm.__version__)"
#   Needs mlx-lm >= 0.25.2, mlx >= 0.27.0 (avoid 0.26.x bfloat16 bug)

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
MODEL="Qwen/Qwen3-8B-MLX-4bit"
DATA_DIR="${PROJECT_DIR}/data"
ADAPTER_DIR="${PROJECT_DIR}/adapters"

# Verify data exists
if [ ! -f "${DATA_DIR}/train.jsonl" ] || [ ! -f "${DATA_DIR}/valid.jsonl" ]; then
    echo "Error: Training data not found at ${DATA_DIR}/train.jsonl"
    echo "Run the data preparation scripts first:"
    echo "  python scripts/download_datasets.py"
    echo "  python scripts/generate_cot_solutions.py"
    echo "  python scripts/format_data.py"
    exit 1
fi

TRAIN_COUNT=$(wc -l < "${DATA_DIR}/train.jsonl" | tr -d ' ')
VALID_COUNT=$(wc -l < "${DATA_DIR}/valid.jsonl" | tr -d ' ')
echo "Training data: ${TRAIN_COUNT} examples"
echo "Validation data: ${VALID_COUNT} examples"

# Create adapter directory
mkdir -p "${ADAPTER_DIR}"

echo ""
echo "============================================================"
echo "Phase 2b: Starting QLoRA SFT with MLX"
echo "  Model: ${MODEL}"
echo "  Data: ${DATA_DIR}"
echo "  Adapters: ${ADAPTER_DIR}"
echo "============================================================"
echo ""

# Run QLoRA fine-tuning
# - 4-bit model (~4.5GB) + LoRA fits in 18GB unified memory
# - Gradient checkpointing saves memory
# - Effective batch size = 4 (1 x 4 accumulation steps)
python -m mlx_lm.lora \
    --model "${MODEL}" \
    --train \
    --data "${DATA_DIR}" \
    --batch-size 1 \
    --num-layers 8 \
    --max-seq-length 2048 \
    --grad-checkpoint \
    --grad-accumulation-steps 4 \
    --iters 3500 \
    --learning-rate 1e-5 \
    --steps-per-report 10 \
    --steps-per-eval 200 \
    --adapter-path "${ADAPTER_DIR}" \
    --save-every 200

echo ""
echo "============================================================"
echo "SFT training complete!"
echo "Adapters saved to: ${ADAPTER_DIR}"
echo ""
echo "Next steps:"
echo "  1. Test: bash scripts/test_sft.sh"
echo "  2. Fuse: bash scripts/fuse_and_export.sh"
echo "============================================================"
