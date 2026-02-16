#!/usr/bin/env python3
"""
Data cleanup script for JEE fine-tuning dataset.

Reads quality_report.json, filters out entries flagged with severity "drop",
backs up original data, and rewrites cleaned train/valid files.

Usage:
    python scripts/clean_data.py             # execute cleanup
    python scripts/clean_data.py --dry-run   # preview only
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
BACKUP_DIR = DATA_DIR / "backup"
REPORT_PATH = DATA_DIR / "quality_report.json"

TRAIN_FULL = DATA_DIR / "train_full.jsonl"
VALID_FULL = DATA_DIR / "valid_full.jsonl"
TRAIN_OUT = DATA_DIR / "train.jsonl"
VALID_OUT = DATA_DIR / "valid.jsonl"


def load_jsonl(path: Path) -> list[dict]:
    """Load a JSONL file."""
    if not path.exists():
        return []
    rows = []
    with open(path) as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def check_staleness(report_path: Path, data_paths: list[Path]) -> bool:
    """Check if quality report is newer than data files."""
    if not report_path.exists():
        return True
    report_mtime = report_path.stat().st_mtime
    for p in data_paths:
        if p.exists() and p.stat().st_mtime > report_mtime:
            print(f"  Warning: {p.name} is newer than quality report")
            return True
    return False


def collect_drop_indices(report: dict) -> set[int]:
    """Collect indices flagged for dropping from quality report."""
    drop_indices = set()
    flags_by_cat = report.get("flags_by_category", {})
    for cat, flags in flags_by_cat.items():
        for flag in flags:
            if flag.get("severity") == "drop" and flag.get("index", -1) >= 0:
                drop_indices.add(flag["index"])
    return drop_indices


def subject_counts(data: list[dict]) -> dict[str, int]:
    """Count entries per subject."""
    counts = {}
    for row in data:
        subj = row.get("metadata", {}).get("subject", "Unknown")
        counts[subj] = counts.get(subj, 0) + 1
    return counts


def main():
    parser = argparse.ArgumentParser(description="Clean JEE training data based on quality report")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    args = parser.parse_args()

    print("=" * 60)
    print("Data Cleanup Script")
    print("=" * 60)

    # Load quality report
    if not REPORT_PATH.exists():
        print(f"Error: {REPORT_PATH} not found.")
        print("Run: python scripts/data_quality_check.py")
        sys.exit(1)

    with open(REPORT_PATH) as f:
        report = json.load(f)

    # Check staleness
    stale = check_staleness(REPORT_PATH, [TRAIN_FULL, VALID_FULL])
    if stale:
        print("  Warning: quality report may be stale. Consider re-running data_quality_check.py")

    # Load data
    train_data = load_jsonl(TRAIN_FULL)
    valid_data = load_jsonl(VALID_FULL)
    print(f"\nLoaded: {len(train_data)} train + {len(valid_data)} valid")

    # Collect drop indices
    drop_indices = collect_drop_indices(report)
    print(f"Indices flagged for drop: {len(drop_indices)}")

    if not drop_indices:
        print("No entries to drop. Data is clean.")
        return

    # Show before counts
    before_subjects = subject_counts(train_data)
    print(f"\nBefore cleanup (train):")
    for subj, count in sorted(before_subjects.items()):
        print(f"  {subj}: {count}")

    # Filter train data (drop indices apply to train_full)
    cleaned_train = []
    dropped_subjects = {}
    for idx, row in enumerate(train_data):
        if idx in drop_indices:
            subj = row.get("metadata", {}).get("subject", "Unknown")
            dropped_subjects[subj] = dropped_subjects.get(subj, 0) + 1
        else:
            cleaned_train.append(row)

    print(f"\nDropped {len(train_data) - len(cleaned_train)} entries:")
    for subj, count in sorted(dropped_subjects.items()):
        print(f"  {subj}: {count}")

    # After counts
    after_subjects = subject_counts(cleaned_train)
    print(f"\nAfter cleanup (train):")
    for subj, count in sorted(after_subjects.items()):
        before = before_subjects.get(subj, 0)
        diff = before - count
        pct = f" (-{diff}, -{diff/before:.1%})" if before > 0 and diff > 0 else ""
        print(f"  {subj}: {count}{pct}")

    print(f"\nTotal: {len(train_data)} -> {len(cleaned_train)} train")

    if args.dry_run:
        print("\n[DRY RUN] No files written.")
        return

    # Backup original files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_subdir = BACKUP_DIR / timestamp
    backup_subdir.mkdir(parents=True, exist_ok=True)

    for src in [TRAIN_FULL, VALID_FULL, TRAIN_OUT, VALID_OUT]:
        if src.exists():
            shutil.copy2(src, backup_subdir / src.name)
    print(f"\nBacked up originals to {backup_subdir}")

    # Write cleaned full files
    with open(TRAIN_FULL, "w") as f:
        for row in cleaned_train:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    # Valid stays the same (drops are train-only indices)
    # But re-write to ensure consistency
    with open(VALID_FULL, "w") as f:
        for row in valid_data:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    # Write stripped versions for mlx-lm
    with open(TRAIN_OUT, "w") as f:
        for row in cleaned_train:
            f.write(json.dumps({"messages": row["messages"]}, ensure_ascii=False) + "\n")

    with open(VALID_OUT, "w") as f:
        for row in valid_data:
            f.write(json.dumps({"messages": row["messages"]}, ensure_ascii=False) + "\n")

    print(f"Wrote cleaned files:")
    print(f"  {TRAIN_OUT} ({len(cleaned_train)} examples)")
    print(f"  {VALID_OUT} ({len(valid_data)} examples)")
    print(f"  {TRAIN_FULL}")
    print(f"  {VALID_FULL}")

    # Re-derive SDPO files
    sdpo_script = PROJECT_DIR / "scripts" / "prepare_sdpo_data.py"
    if sdpo_script.exists():
        print("\nRe-deriving SDPO data...")
        result = subprocess.run(
            [sys.executable, str(sdpo_script)],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            print("  SDPO data updated successfully.")
        else:
            print(f"  Warning: SDPO script failed: {result.stderr[:200]}")
    else:
        print(f"\n  Warning: {sdpo_script} not found, skipping SDPO re-derivation")

    print("\nCleanup complete.")


if __name__ == "__main__":
    main()
