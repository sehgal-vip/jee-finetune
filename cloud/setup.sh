#!/usr/bin/env bash
# Phase 3a-3b: Cloud GPU environment setup for SDPO training
#
# Run this on your cloud GPU instance (Colab, Lambda, RunPod, etc.)
# Minimum: 1x GPU with 40GB+ VRAM (A100 recommended)

set -euo pipefail

echo "============================================================"
echo "Phase 3: Setting up SDPO training environment"
echo "============================================================"

# 1. System check
echo ""
echo "[1/5] Checking GPU..."
nvidia-smi || { echo "Error: No NVIDIA GPU found"; exit 1; }

# 2. Install base dependencies
echo ""
echo "[2/5] Installing Python dependencies..."
pip install --upgrade pip
pip install torch transformers accelerate peft trl datasets
pip install huggingface_hub anthropic vllm
pip install pandas tqdm jsonlines regex wandb

# 3. Clone and install SDPO
echo ""
echo "[3/5] Setting up SDPO..."
if [ ! -d "SDPO" ]; then
    git clone https://github.com/lasgroup/SDPO.git
fi
cd SDPO
pip install -e .
cd ..

# 4. Install verl (SDPO's RL training framework)
echo ""
echo "[4/5] Installing verl..."
pip install verl

# 5. Download the SFT model from HuggingFace
echo ""
echo "[5/5] Downloading SFT model..."
HF_USERNAME="${HF_USERNAME:-}"
if [ -n "${HF_USERNAME}" ]; then
    python -c "
from huggingface_hub import snapshot_download
snapshot_download('${HF_USERNAME}/qwen3-8b-jee-sft', local_dir='./qwen3-8b-jee-sft')
print('Model downloaded to ./qwen3-8b-jee-sft')
"
else
    echo "Warning: HF_USERNAME not set. Set it to download your SFT model:"
    echo "  export HF_USERNAME='your-username'"
fi

echo ""
echo "============================================================"
echo "Setup complete! Next:"
echo "  1. Set API keys: export ANTHROPIC_API_KEY='...'"
echo "  2. Upload SDPO data: scp data/sdpo/* cloud:sdpo_data/"
echo "  3. Run training: python train_sdpo.py"
echo "============================================================"
