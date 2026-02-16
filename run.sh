#!/usr/bin/env bash
# Master run script for IIT JEE Fine-Tuning Pipeline
#
# Usage:
#   ./run.sh phase1     # Download + prep data
#   ./run.sh phase2     # SFT training on Mac
#   ./run.sh phase3     # (run on cloud GPU)
#   ./run.sh phase4     # Inference on Mac
#   ./run.sh eval-sft   # Evaluate SFT model
#   ./run.sh eval-sdpo  # Evaluate SDPO model
#   ./run.sh compare    # Compare SFT vs SDPO

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "${PROJECT_DIR}"

usage() {
    echo "Usage: $0 <command>"
    echo ""
    echo "Commands:"
    echo "  phase1       Download datasets + generate CoT + format data"
    echo "  phase2       SFT training with QLoRA on Mac (MLX)"
    echo "  phase3-prep  Package data for cloud SDPO training"
    echo "  phase4       Convert SDPO model to MLX + serve"
    echo "  eval-sft     Evaluate the SFT model"
    echo "  eval-sdpo    Evaluate the SDPO model"
    echo "  compare      Compare SFT vs SDPO results"
    echo "  serve        Start local inference server"
    echo ""
    echo "Typical workflow:"
    echo "  1. ./run.sh phase1"
    echo "  2. ./run.sh phase2"
    echo "  3. ./run.sh phase3-prep  (then run cloud/setup.sh + cloud/train_sdpo.py on GPU)"
    echo "  4. ./run.sh phase4"
    echo "  5. ./run.sh eval-sft && ./run.sh eval-sdpo && ./run.sh compare"
}

case "${1:-}" in
    phase1)
        echo "=== Phase 1: Data Preparation ==="
        echo ""
        echo "[Step 1/4] Downloading datasets..."
        python scripts/download_datasets.py

        echo ""
        echo "[Step 2/4] Generating CoT solutions (requires ANTHROPIC_API_KEY)..."
        if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
            echo "Warning: ANTHROPIC_API_KEY not set. Skipping CoT generation."
            echo "Set it and re-run: export ANTHROPIC_API_KEY='your-key'"
        else
            python scripts/generate_cot_solutions.py
        fi

        echo ""
        echo "[Step 3/4] Formatting data for training..."
        python scripts/format_data.py

        echo ""
        echo "[Step 4/4] Preparing SDPO data..."
        python scripts/prepare_sdpo_data.py

        echo ""
        echo "Phase 1 complete! Check data/ directory."
        ;;

    phase2)
        echo "=== Phase 2: SFT Training on Mac ==="
        bash scripts/train_sft.sh

        echo ""
        echo "Testing SFT model..."
        bash scripts/test_sft.sh

        echo ""
        echo "Fusing and exporting..."
        bash scripts/fuse_and_export.sh
        ;;

    phase3-prep)
        echo "=== Packaging data for cloud SDPO training ==="
        CLOUD_PKG="${PROJECT_DIR}/cloud_package"
        mkdir -p "${CLOUD_PKG}/sdpo_data"

        # Copy SDPO data
        cp data/sdpo/*.jsonl "${CLOUD_PKG}/sdpo_data/"
        cp data/sdpo/judge_config.json "${CLOUD_PKG}/sdpo_data/"

        # Copy cloud scripts
        cp cloud/setup.sh "${CLOUD_PKG}/"
        cp cloud/train_sdpo.py "${CLOUD_PKG}/"
        cp cloud/judge.py "${CLOUD_PKG}/"
        cp cloud/sdpo_config.yaml "${CLOUD_PKG}/"
        cp requirements-cloud.txt "${CLOUD_PKG}/"

        echo "Cloud package created at: ${CLOUD_PKG}/"
        echo ""
        echo "Upload to your cloud instance:"
        echo "  scp -r ${CLOUD_PKG}/* <cloud-host>:~/jee-sdpo/"
        echo ""
        echo "Then on the cloud:"
        echo "  cd ~/jee-sdpo && bash setup.sh && python train_sdpo.py"
        ;;

    phase4)
        echo "=== Phase 4: Convert + Inference on Mac ==="
        bash scripts/convert_to_mlx.sh
        ;;

    eval-sft)
        echo "=== Evaluating SFT model ==="
        python evaluation/evaluate.py \
            --model "Qwen/Qwen3-8B-MLX-4bit" \
            --adapter-path ./adapters \
            --name "sft" \
            --limit 200
        ;;

    eval-sdpo)
        echo "=== Evaluating SDPO model ==="
        python evaluation/evaluate.py \
            --model "./qwen3-8b-jee-sdpo-mlx-4bit" \
            --name "sdpo" \
            --limit 200
        ;;

    compare)
        echo "=== Comparing SFT vs SDPO ==="
        python evaluation/compare.py \
            evaluation/results_sft.json \
            evaluation/results_sdpo.json
        ;;

    serve)
        bash scripts/serve.sh "${2:-8080}"
        ;;

    *)
        usage
        ;;
esac
