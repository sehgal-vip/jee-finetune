#!/usr/bin/env bash
# Phase 4a: Convert SDPO-trained model to MLX format for Mac inference
#
# After downloading the SDPO-trained model from the cloud,
# convert it to 4-bit MLX format for efficient local inference.

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
INPUT_DIR="${1:-${PROJECT_DIR}/qwen3-8b-jee-sdpo}"
OUTPUT_DIR="${PROJECT_DIR}/qwen3-8b-jee-sdpo-mlx-4bit"

if [ ! -d "${INPUT_DIR}" ]; then
    echo "Error: Model directory not found: ${INPUT_DIR}"
    echo "Usage: $0 [model_path]"
    echo ""
    echo "Download from cloud first, or pass the path to the SDPO model."
    exit 1
fi

echo "============================================================"
echo "Phase 4a: Converting SDPO model to MLX 4-bit format"
echo "  Input:  ${INPUT_DIR}"
echo "  Output: ${OUTPUT_DIR}"
echo "============================================================"

mlx_lm.convert \
    --hf-path "${INPUT_DIR}" \
    -q --q-bits 4 \
    --q-group-size 64 \
    --mlx-path "${OUTPUT_DIR}"

echo ""
echo "Conversion complete!"
echo "Model saved to: ${OUTPUT_DIR}"
echo ""
echo "Test with:"
echo "  python -m mlx_lm.generate --model ${OUTPUT_DIR} --prompt 'Solve: ...'"
