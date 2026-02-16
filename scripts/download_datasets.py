#!/usr/bin/env python3
"""
Phase 1a: Download seed datasets for IIT JEE fine-tuning.

Downloads:
  - JEEBench (515 JEE Advanced questions)
  - SciInstruct (254K physics/chemistry/math CoT samples)
  - NuminaMath (860K competition math problems)
  - Kaggle JEE JSON (structured JEE questions)
"""

import json
import os
import sys
from pathlib import Path

from datasets import load_dataset
from huggingface_hub import hf_hub_download, snapshot_download
from tqdm import tqdm

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"


def download_jeebench():
    """Download JEEBench dataset — 515 JEE Advanced questions."""
    print("\n[1/4] Downloading JEEBench...")
    out_dir = RAW_DIR / "jeebench"
    out_dir.mkdir(parents=True, exist_ok=True)

    ds = load_dataset("daman1209arora/jeebench", trust_remote_code=True)
    records = []
    for split in ds:
        for row in tqdm(ds[split], desc=f"  jeebench/{split}"):
            records.append(dict(row))

    out_path = out_dir / "jeebench.jsonl"
    with open(out_path, "w") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"  Saved {len(records)} questions to {out_path}")
    return records


def download_sciinstruct():
    """Download SciInstruct dataset from THUDM/SciGLM."""
    print("\n[2/4] Downloading SciInstruct...")
    out_dir = RAW_DIR / "sciinstruct"
    out_dir.mkdir(parents=True, exist_ok=True)

    # SciInstruct is available on HuggingFace as THUDM/SciInstruct
    try:
        ds = load_dataset("THUDM/SciInstruct", trust_remote_code=True)
        records = []
        for split in ds:
            for row in tqdm(ds[split], desc=f"  sciinstruct/{split}"):
                records.append(dict(row))

        out_path = out_dir / "sciinstruct.jsonl"
        with open(out_path, "w") as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"  Saved {len(records)} samples to {out_path}")
        return records
    except Exception as e:
        print(f"  Warning: Could not load SciInstruct from HF: {e}")
        print("  Trying alternative: downloading from GitHub...")
        try:
            snapshot_download(
                "THUDM/SciInstruct",
                local_dir=str(out_dir),
                repo_type="dataset",
            )
            print(f"  Downloaded SciInstruct to {out_dir}")
        except Exception as e2:
            print(f"  Could not download SciInstruct: {e2}")
            print("  You can manually download from https://github.com/THUDM/SciGLM")
        return []


def download_numinamath():
    """Download NuminaMath dataset — 860K competition math problems."""
    print("\n[3/4] Downloading NuminaMath...")
    out_dir = RAW_DIR / "numinamath"
    out_dir.mkdir(parents=True, exist_ok=True)

    # NuminaMath-CoT is the version with chain-of-thought solutions
    ds = load_dataset("AI-MO/NuminaMath-CoT", trust_remote_code=True)
    records = []
    for split in ds:
        for row in tqdm(ds[split], desc=f"  numinamath/{split}"):
            records.append(dict(row))

    out_path = out_dir / "numinamath.jsonl"
    with open(out_path, "w") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"  Saved {len(records)} problems to {out_path}")
    return records


def download_kaggle_jee():
    """Download Kaggle JEE JSON dataset."""
    print("\n[4/4] Downloading Kaggle JEE JSON...")
    out_dir = RAW_DIR / "kaggle_jee"
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        ds = load_dataset("damerajee/jee-question-json-format", trust_remote_code=True)
        records = []
        for split in ds:
            for row in tqdm(ds[split], desc=f"  kaggle_jee/{split}"):
                records.append(dict(row))

        out_path = out_dir / "kaggle_jee.jsonl"
        with open(out_path, "w") as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"  Saved {len(records)} questions to {out_path}")
        return records
    except Exception as e:
        print(f"  Warning: Could not load Kaggle JEE: {e}")
        print("  This dataset may require Kaggle authentication.")
        print("  Continuing without it...")
        return []


def main():
    print("=" * 60)
    print("Phase 1a: Downloading seed datasets for IIT JEE fine-tuning")
    print("=" * 60)

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    stats = {}

    jeebench = download_jeebench()
    stats["jeebench"] = len(jeebench)

    sciinstruct = download_sciinstruct()
    stats["sciinstruct"] = len(sciinstruct)

    numinamath = download_numinamath()
    stats["numinamath"] = len(numinamath)

    kaggle_jee = download_kaggle_jee()
    stats["kaggle_jee"] = len(kaggle_jee)

    print("\n" + "=" * 60)
    print("Download Summary:")
    for name, count in stats.items():
        print(f"  {name}: {count:,} records")
    print(f"  Total: {sum(stats.values()):,} records")
    print(f"  Location: {RAW_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
