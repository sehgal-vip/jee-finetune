#!/usr/bin/env bash
# Phase 4b: Serve the final model as a local API
#
# Starts an OpenAI-compatible API server on localhost.

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PORT="${1:-8080}"

# Try SDPO model first, fall back to SFT-only model
if [ -d "${PROJECT_DIR}/qwen3-8b-jee-sdpo-mlx-4bit" ]; then
    MODEL_DIR="${PROJECT_DIR}/qwen3-8b-jee-sdpo-mlx-4bit"
    echo "Serving SDPO model"
elif [ -d "${PROJECT_DIR}/adapters" ] && [ -f "${PROJECT_DIR}/adapters/adapters.safetensors" ]; then
    MODEL_DIR="Qwen/Qwen3-8B-MLX-4bit"
    ADAPTER_FLAG="--adapter-path ${PROJECT_DIR}/adapters"
    echo "Serving SFT model (with adapters)"
else
    MODEL_DIR="Qwen/Qwen3-8B-MLX-4bit"
    echo "Serving base model (no fine-tuning detected)"
fi

echo "============================================================"
echo "Starting model server on http://localhost:${PORT}"
echo "  Model: ${MODEL_DIR}"
echo ""
echo "  Usage: curl http://localhost:${PORT}/v1/chat/completions \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"messages\": [{\"role\": \"user\", \"content\": \"Solve: ...\"}]}'"
echo "============================================================"

python -m mlx_lm.server \
    --model "${MODEL_DIR}" \
    ${ADAPTER_FLAG:-} \
    --port "${PORT}"
