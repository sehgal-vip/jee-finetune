#!/usr/bin/env python3
"""
Compare evaluation results between SFT and SDPO models.

Loads two result JSON files and produces a side-by-side comparison report.
"""

import json
import sys
from pathlib import Path


def load_results(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def compare(sft_path: str, sdpo_path: str):
    sft = load_results(sft_path)
    sdpo = load_results(sdpo_path)

    print("=" * 70)
    print(f"{'Metric':<30} {'SFT':>15} {'SDPO':>15} {'Delta':>8}")
    print("=" * 70)

    # Overall
    sft_acc = sft["correct"] / max(sft["total"], 1) * 100
    sdpo_acc = sdpo["correct"] / max(sdpo["total"], 1) * 100
    delta = sdpo_acc - sft_acc
    print(f"{'Overall Accuracy':<30} {sft_acc:>14.1f}% {sdpo_acc:>14.1f}% {delta:>+7.1f}%")

    print("-" * 70)

    # By subject
    all_subjects = sorted(
        set(list(sft.get("by_subject", {}).keys()) + list(sdpo.get("by_subject", {}).keys()))
    )
    for subject in all_subjects:
        sft_s = sft.get("by_subject", {}).get(subject, {"total": 0, "correct": 0})
        sdpo_s = sdpo.get("by_subject", {}).get(subject, {"total": 0, "correct": 0})
        sft_a = sft_s["correct"] / max(sft_s["total"], 1) * 100
        sdpo_a = sdpo_s["correct"] / max(sdpo_s["total"], 1) * 100
        d = sdpo_a - sft_a
        print(f"  {subject:<28} {sft_a:>14.1f}% {sdpo_a:>14.1f}% {d:>+7.1f}%")

    print("-" * 70)

    # By question type
    all_types = sorted(
        set(list(sft.get("by_type", {}).keys()) + list(sdpo.get("by_type", {}).keys()))
    )
    if all_types:
        for q_type in all_types:
            sft_t = sft.get("by_type", {}).get(q_type, {"total": 0, "correct": 0})
            sdpo_t = sdpo.get("by_type", {}).get(q_type, {"total": 0, "correct": 0})
            sft_a = sft_t["correct"] / max(sft_t["total"], 1) * 100
            sdpo_a = sdpo_t["correct"] / max(sdpo_t["total"], 1) * 100
            d = sdpo_a - sft_a
            print(f"  {q_type:<28} {sft_a:>14.1f}% {sdpo_a:>14.1f}% {d:>+7.1f}%")

    print("=" * 70)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare.py <sft_results.json> <sdpo_results.json>")
        sys.exit(1)
    compare(sys.argv[1], sys.argv[2])
