#!/usr/bin/env python3
"""
Evaluation: Benchmark the model on JEEBench and held-out questions.

Measures accuracy by subject and question type, compares SFT vs SDPO
performance, and generates a detailed report.
"""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from tqdm import tqdm

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
EVAL_DIR = Path(__file__).resolve().parent


def generate_response(prompt: str, model_path: str, adapter_path: str = None) -> str:
    """Generate a response using mlx_lm.generate."""
    cmd = [
        sys.executable, "-m", "mlx_lm.generate",
        "--model", model_path,
        "--max-tokens", "2048",
        "--prompt", prompt,
    ]
    if adapter_path:
        cmd.extend(["--adapter-path", adapter_path])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        return "[ERROR: generation timed out after 300s]"
    if result.returncode != 0:
        return f"[ERROR: {result.stderr[:200]}]"
    return result.stdout.strip()


def extract_answer(response: str) -> str:
    """Extract the final answer from a response."""
    # Pattern 0: \boxed{...} — take the LAST occurrence (definitive answer)
    all_boxed = list(re.finditer(r"\\boxed\{", response))
    if all_boxed:
        match = all_boxed[-1]
        start = match.end()
        depth = 1
        i = start
        while i < len(response) and depth > 0:
            if response[i] == "{":
                depth += 1
            elif response[i] == "}":
                depth -= 1
            i += 1
        if depth == 0:
            return response[start:i-1].strip()

    # Pattern 1: **Answer:** ...
    match = re.search(r"\*\*Answer:\*\*\s*(.+?)(?:\n|$)", response)
    if match:
        return match.group(1).strip()

    # Pattern 2: Answer: ...
    match = re.search(r"(?:^|\n)\s*Answer:\s*(.+?)(?:\n|$)", response)
    if match:
        return match.group(1).strip()

    # Pattern 3: The answer is ...
    match = re.search(r"[Tt]he\s+answer\s+is\s+(.+?)(?:\.|$)", response)
    if match:
        return match.group(1).strip()

    # Pattern 4: Last MCQ option
    lines = response.strip().split("\n")
    for line in reversed(lines):
        match = re.search(r"\(([A-D])\)", line)
        if match:
            return match.group(1)

    # Pattern 5: Last "= <number>" in derivation (e.g., "= 2.5" or "= 3.14 \times 10^{5}")
    all_eq = re.findall(
        r"=\s*(-?[\d]+\.?[\d]*(?:\s*\\?times\s*10\^?\{?-?[\d.]+\}?)?)",
        response,
    )
    if all_eq:
        return all_eq[-1].strip()

    return ""


def normalize_answer(answer: str) -> str:
    """Normalize an answer for comparison."""
    answer = answer.strip().lower()
    answer = re.sub(r"^\((.+)\)$", r"\1", answer)
    answer = re.sub(r"^\$(.+)\$$", r"\1", answer)
    # Strip \text{...} and \mathrm{...} wrappers BEFORE removing \ { }
    # so their letters don't pollute numeric/MCQ matching
    answer = re.sub(r"\\text\{([^}]*)\}", r"\1", answer)
    answer = re.sub(r"\\mathrm\{([^}]*)\}", r"\1", answer)
    answer = re.sub(r"[\\{}\s]", "", answer)
    return answer


def _parse_number(s: str) -> float | None:
    """Parse a number from a normalized string, handling scientific notation.

    Handles patterns like: '2.5', '-3', '2.5times10^3', '2.5times10^{-3}',
    '2.5e3', and plain digits.
    """
    # Try scientific notation: N \times 10^{exp} (after normalization, no backslashes)
    m = re.search(r"(-?[\d.]+)\s*times\s*10\^?\{?(-?[\d.]+)\}?", s)
    if m:
        try:
            return float(m.group(1)) * (10 ** float(m.group(2)))
        except (ValueError, OverflowError):
            pass

    # Try extracting a plain number (digits, dots, minus, and 'e' for 1.5e3)
    m = re.search(r"-?[\d]+\.?[\d]*(?:e[+-]?[\d]+)?", s)
    if m:
        try:
            return float(m.group(0))
        except ValueError:
            pass

    return None


def check_single_answer(gen: str, gt: str) -> bool:
    """Check if a single normalized generated answer matches a single ground truth."""
    if not gen or not gt:
        return False

    if gen == gt or gt in gen or gen in gt:
        return True

    # Numeric comparison with 2% tolerance
    gen_num = _parse_number(gen)
    gt_num = _parse_number(gt)
    if gen_num is not None and gt_num is not None:
        if gt_num != 0:
            return abs(gen_num - gt_num) / abs(gt_num) < 0.02
        return abs(gen_num - gt_num) < 1e-6

    # MCQ letter comparison — standalone letters only
    gen_letters = set(re.findall(r"\b([a-d])\b", gen))
    gt_letters = set(re.findall(r"\b([a-d])\b", gt))
    if gen_letters and gt_letters:
        return gen_letters == gt_letters

    return False


def check_answer(generated: str, ground_truth: str) -> bool:
    """Check if generated answer matches ground truth.

    Handles single answers and multi-part JSON array ground truths.
    For JSON arrays, requires majority of parts to match.
    """
    gt_str = str(ground_truth).strip()

    # Detect JSON array ground truths like ["ans1", "ans2", ...]
    if gt_str.startswith("["):
        try:
            parts = json.loads(gt_str)
            if isinstance(parts, list) and len(parts) > 1:
                gen = normalize_answer(generated)
                matches = sum(
                    1 for part in parts
                    if check_single_answer(gen, normalize_answer(str(part)))
                )
                # Majority match (more than half)
                return matches > len(parts) / 2
        except (json.JSONDecodeError, TypeError):
            pass

    # Single answer comparison
    gen = normalize_answer(generated)
    gt = normalize_answer(gt_str)
    return check_single_answer(gen, gt)


def evaluate_model(
    model_path: str,
    eval_data: list[dict],
    model_name: str = "model",
    adapter_path: str = None,
) -> dict:
    """Evaluate a model on a set of questions."""
    results = {
        "model_name": model_name,
        "total": 0,
        "correct": 0,
        "by_subject": {},
        "by_type": {},
        "details": [],
    }

    for item in tqdm(eval_data, desc=f"Evaluating {model_name}"):
        question = item.get("prompt", item.get("question", ""))
        ground_truth = item.get("ground_truth", item.get("answer", ""))
        subject = item.get("subject", "Unknown")
        q_type = item.get("question_type", "")

        if not question or not ground_truth:
            continue

        response = generate_response(question, model_path, adapter_path)
        extracted = extract_answer(response)
        is_correct = check_answer(extracted, ground_truth)

        results["total"] += 1
        if is_correct:
            results["correct"] += 1

        # By subject
        if subject not in results["by_subject"]:
            results["by_subject"][subject] = {"total": 0, "correct": 0}
        results["by_subject"][subject]["total"] += 1
        if is_correct:
            results["by_subject"][subject]["correct"] += 1

        # By type
        if q_type:
            if q_type not in results["by_type"]:
                results["by_type"][q_type] = {"total": 0, "correct": 0}
            results["by_type"][q_type]["total"] += 1
            if is_correct:
                results["by_type"][q_type]["correct"] += 1

        # Print running accuracy summary
        total_so_far = results["total"]
        correct_so_far = results["correct"]
        pct = correct_so_far / total_so_far * 100
        status = "CORRECT" if is_correct else "WRONG  "
        subj_parts = []
        for s, st in sorted(results["by_subject"].items()):
            # Use abbreviated subject names (first 4 chars)
            abbr = s[:4]
            subj_parts.append(f"{abbr}: {st['correct']}/{st['total']}")
        print(
            f"[{total_so_far:>3}/{len(eval_data)}] {status}  {subject:<12s}"
            f" | Overall: {correct_so_far}/{total_so_far} ({pct:.1f}%)"
            f" | {' '.join(subj_parts)}",
            flush=True,
        )

        results["details"].append({
            "question": question[:200],
            "ground_truth": ground_truth,
            "extracted_answer": extracted,
            "is_correct": is_correct,
            "subject": subject,
            "response_length": len(response),
        })

    return results


def print_report(results: dict):
    """Print a formatted evaluation report."""
    total = results["total"]
    correct = results["correct"]
    accuracy = correct / max(total, 1) * 100

    print(f"\n{'='*60}")
    print(f"Evaluation Report: {results['model_name']}")
    print(f"{'='*60}")
    print(f"Overall: {correct}/{total} ({accuracy:.1f}%)")

    print(f"\nBy Subject:")
    for subject, stats in sorted(results["by_subject"].items()):
        acc = stats["correct"] / max(stats["total"], 1) * 100
        print(f"  {subject}: {stats['correct']}/{stats['total']} ({acc:.1f}%)")

    if results["by_type"]:
        print(f"\nBy Question Type:")
        for q_type, stats in sorted(results["by_type"].items()):
            acc = stats["correct"] / max(stats["total"], 1) * 100
            print(f"  {q_type}: {stats['correct']}/{stats['total']} ({acc:.1f}%)")

    print(f"{'='*60}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate JEE model")
    parser.add_argument("--model", required=True, help="Path to the model")
    parser.add_argument("--adapter-path", default=None, help="Path to LoRA adapters")
    parser.add_argument("--eval-data", default=None, help="Path to evaluation JSONL")
    parser.add_argument("--name", default="model", help="Name for the report")
    parser.add_argument("--output", default=None, help="Save results to JSON file")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of questions (0=all)")
    args = parser.parse_args()

    # Load evaluation data
    eval_path = args.eval_data
    if eval_path is None:
        # Try SDPO eval prompts first, then validation data
        sdpo_eval = DATA_DIR / "sdpo" / "eval_prompts.jsonl"
        valid_data = DATA_DIR / "valid_full.jsonl"
        if sdpo_eval.exists():
            eval_path = str(sdpo_eval)
        elif valid_data.exists():
            eval_path = str(valid_data)
        else:
            print("Error: No evaluation data found.")
            print("Specify with --eval-data or run data preparation first.")
            sys.exit(1)

    eval_data = []
    with open(eval_path) as f:
        for line in f:
            if line.strip():
                eval_data.append(json.loads(line))

    if args.limit > 0:
        eval_data = eval_data[: args.limit]

    print(f"Evaluating on {len(eval_data)} questions from {eval_path}")

    results = evaluate_model(
        model_path=args.model,
        eval_data=eval_data,
        model_name=args.name,
        adapter_path=args.adapter_path,
    )

    print_report(results)

    # Save results
    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nDetailed results saved to {args.output}")
    else:
        default_output = EVAL_DIR / f"results_{args.name}.json"
        with open(default_output, "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nDetailed results saved to {default_output}")


if __name__ == "__main__":
    main()
