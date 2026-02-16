#!/usr/bin/env bash
# Phase 2d: Fuse LoRA adapters into full model and upload to HuggingFace
#
# This de-quantizes the model so it can be used with PyTorch/transformers
# on the cloud GPU for SDPO training.

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
MODEL="Qwen/Qwen3-8B-MLX-4bit"
ADAPTER_DIR="${PROJECT_DIR}/adapters"
FUSED_DIR="${PROJECT_DIR}/qwen3-8b-jee-sft"

# Check for HF username
HF_USERNAME="${HF_USERNAME:-}"
if [ -z "${HF_USERNAME}" ]; then
    echo "Warning: HF_USERNAME not set. Will fuse but skip upload."
    echo "Set it: export HF_USERNAME='your-username'"
fi

if [ ! -d "${ADAPTER_DIR}" ] || [ ! -f "${ADAPTER_DIR}/adapters.safetensors" ]; then
    echo "Error: No trained adapters found at ${ADAPTER_DIR}"
    echo "Run training first: bash scripts/train_sft.sh"
    exit 1
fi

echo "============================================================"
echo "Phase 2d: Fusing adapters and exporting model"
echo "  Model: ${MODEL}"
echo "  Adapters: ${ADAPTER_DIR}"
echo "  Output: ${FUSED_DIR}"
echo "============================================================"

# Fuse adapters into full (de-quantized) model
mlx_lm.fuse \
    --model "${MODEL}" \
    --adapter-path "${ADAPTER_DIR}" \
    --save-path "${FUSED_DIR}" \
    --dequantize

echo "Fused model saved to: ${FUSED_DIR}"

# Upload to HuggingFace (private repo) if username is set
if [ -n "${HF_USERNAME}" ]; then
    REPO_NAME="${HF_USERNAME}/qwen3-8b-jee-sft"
    echo ""
    echo "Uploading to HuggingFace: ${REPO_NAME}"
    huggingface-cli upload "${REPO_NAME}" "${FUSED_DIR}" --private
    echo "Upload complete: https://huggingface.co/${REPO_NAME}"
else
    echo ""
    echo "Skipping HuggingFace upload (HF_USERNAME not set)."
    echo "To upload manually:"
    echo "  export HF_USERNAME='your-username'"
    echo "  huggingface-cli upload \${HF_USERNAME}/qwen3-8b-jee-sft ${FUSED_DIR} --private"
fi

echo ""
echo "============================================================"
echo "Next: Set up cloud GPU for SDPO training (Phase 3)"
echo "============================================================"
