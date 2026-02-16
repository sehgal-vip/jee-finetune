#!/usr/bin/env bash
# Phase 2c: Test the SFT fine-tuned model locally
#
# Runs a few JEE test questions through the adapter-augmented model
# to verify training quality before fusing.

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
MODEL="Qwen/Qwen3-8B-MLX-4bit"
ADAPTER_DIR="${PROJECT_DIR}/adapters"

if [ ! -d "${ADAPTER_DIR}" ] || [ ! -f "${ADAPTER_DIR}/adapters.safetensors" ]; then
    echo "Error: No trained adapters found at ${ADAPTER_DIR}"
    echo "Run training first: bash scripts/train_sft.sh"
    exit 1
fi

echo "============================================================"
echo "Phase 2c: Testing SFT model"
echo "  Model: ${MODEL}"
echo "  Adapters: ${ADAPTER_DIR}"
echo "============================================================"

# Test questions spanning Physics, Chemistry, Mathematics
declare -a PROMPTS=(
    "A particle of mass 2 kg is projected vertically upward with a speed of 20 m/s. Find the maximum height reached by the particle. (Take g = 10 m/s²)"
    "Calculate the pH of a 0.01 M HCl solution at 25°C."
    "Find the area enclosed between the curves y = x² and y = 2x - x² for x ≥ 0."
)

declare -a SUBJECTS=(
    "Physics"
    "Chemistry"
    "Mathematics"
)

for i in "${!PROMPTS[@]}"; do
    echo ""
    echo "------------------------------------------------------------"
    echo "[${SUBJECTS[$i]}] ${PROMPTS[$i]}"
    echo "------------------------------------------------------------"
    python -m mlx_lm.generate \
        --model "${MODEL}" \
        --adapter-path "${ADAPTER_DIR}" \
        --max-tokens 1024 \
        --prompt "${PROMPTS[$i]}"
    echo ""
done

echo "============================================================"
echo "Manual review: Check that solutions show step-by-step reasoning"
echo "with correct LaTeX and arrive at the right answer."
echo "============================================================"
