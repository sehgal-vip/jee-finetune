#!/usr/bin/env python3
"""
Data quality checks for JEE fine-tuning dataset.

Checks ~3,500 processed training examples across 8 categories:
  1. Semantic & answer quality (30%)
  2. Difficulty & topic distribution (scored under #5)
  3. Contamination (25%)
  4. Token length & reasoning quality (15%)
  5. Coverage & diversity (15%)
  6. LaTeX validation (10%)
  7. Schema validation (5% — gate)
  8. Raw dataset inventory (not scored)

Usage:
    python scripts/data_quality_check.py                 # full run
    python scripts/data_quality_check.py --skip-tokenize # skip token counting
    python scripts/data_quality_check.py --skip-raw      # skip raw inventory
    python scripts/data_quality_check.py --sample 20     # manual review dump
    python scripts/data_quality_check.py -v              # verbose
"""

import argparse
import collections
import difflib
import hashlib
import json
import math
import os
import random
import re
import sys
import unicodedata
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
SCRIPTS_DIR = PROJECT_DIR / "scripts"

TRAIN_FULL = DATA_DIR / "train_full.jsonl"
VALID_FULL = DATA_DIR / "valid_full.jsonl"
SDPO_RL = DATA_DIR / "sdpo" / "rl_prompts.jsonl"
SDPO_EVAL = DATA_DIR / "sdpo" / "eval_prompts.jsonl"

REPORT_PATH = DATA_DIR / "quality_report.json"
SAMPLE_PATH = DATA_DIR / "quality_sample.md"

# Benchmark paths — extend this list to add more eval sets
BENCHMARK_PATHS = [
    ("jeebench", RAW_DIR / "jeebench" / "jeebench.jsonl"),
    # HuggingFace arrow datasets handled specially
    ("jee_mains_2025", RAW_DIR / "jee" / "jee_mains_2025"),
    ("jee_main_2025_math", RAW_DIR / "jee" / "jee_main_2025_math"),
]

# ---------------------------------------------------------------------------
# Import reusable code from format_data.py
# ---------------------------------------------------------------------------
sys.path.insert(0, str(SCRIPTS_DIR))
try:
    from format_data import (
        SYSTEM_MESSAGE,
        JEE_PHYSICS_KEYWORDS,
        JEE_CHEMISTRY_KEYWORDS,
        JEE_MATH_KEYWORDS,
        classify_subject,
    )
except ImportError:
    # Fallback if format_data not on path
    SYSTEM_MESSAGE = (
        "You are an expert IIT JEE tutor. Solve problems step-by-step using LaTeX notation. "
        "Show all work clearly and arrive at the final answer."
    )
    JEE_PHYSICS_KEYWORDS = []
    JEE_CHEMISTRY_KEYWORDS = []
    JEE_MATH_KEYWORDS = []

    def classify_subject(text: str) -> str:
        return "Unknown"


# ---------------------------------------------------------------------------
# Colour helpers
# ---------------------------------------------------------------------------
_COLOURS = os.environ.get("NO_COLOR") is None and sys.stdout.isatty()


def _c(code: str, text: str) -> str:
    if _COLOURS:
        return f"\033[{code}m{text}\033[0m"
    return text


def PASS(msg: str) -> str:
    return _c("32", f"[PASS] {msg}")


def WARN(msg: str) -> str:
    return _c("33", f"[WARN] {msg}")


def FAIL(msg: str) -> str:
    return _c("31", f"[FAIL] {msg}")


def INFO(msg: str) -> str:
    return _c("36", f"[INFO] {msg}")


def HEADER(msg: str) -> str:
    return _c("1;35", msg)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    with open(path) as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def load_hf_dataset(path: Path) -> list[dict]:
    """Load a HuggingFace arrow dataset from disk."""
    if not path.exists():
        return []
    try:
        from datasets import load_from_disk
        ds = load_from_disk(str(path))
        # Flatten DatasetDict
        rows = []
        if hasattr(ds, "keys"):
            for split in ds:
                rows.extend(ds[split].to_list())
        else:
            rows = ds.to_list()
        return rows
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Text normalisation helpers
# ---------------------------------------------------------------------------
def normalise_text(text: str) -> str:
    """Collapse whitespace, lowercase, strip LaTeX spacing."""
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalise_latex(text: str) -> str:
    """Normalise LaTeX for comparison: dfrac->frac, whitespace, pi variants."""
    t = text
    t = re.sub(r"\\[dt]frac", r"\\frac", t)
    t = re.sub(r"\s+", "", t)
    # Normalise pi/4 ↔ \frac{\pi}{4}
    t = re.sub(r"\\pi\s*/\s*(\d+)", r"\\frac{\\pi}{\1}", t)
    return t


def strip_structural(text: str) -> str:
    """Strip numbers and variable names, keep operators + LaTeX commands."""
    # Replace numbers with #
    t = re.sub(r"\d+\.?\d*", "#", text)
    # Replace single-letter variables with _
    t = re.sub(r"(?<![\\a-zA-Z])[a-zA-Z](?![a-zA-Z])", "_", t)
    return t


def text_hash(text: str) -> str:
    n = normalise_text(text)
    return hashlib.md5(n.encode()).hexdigest()


def ngram_set(text: str, n: int = 3) -> set:
    tokens = normalise_text(text).split()
    if len(tokens) < n:
        return {normalise_text(text)}
    return {" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


# ---------------------------------------------------------------------------
# Boxed-answer extraction
# ---------------------------------------------------------------------------
_BOXED_RE = re.compile(r"\\boxed\{")


def extract_boxed(text: str) -> str | None:
    """Extract content of \\boxed{...}, handling nested braces. Returns None if no \\boxed."""
    m = _BOXED_RE.search(text)
    if not m:
        return None
    start = m.end()
    depth = 1
    i = start
    while i < len(text) and depth > 0:
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
        i += 1
    return text[start : i - 1] if depth == 0 else text[start:]


def has_answer_marker(text: str) -> bool:
    return bool(re.search(r"(?:^|\n)\s*\*?\*?Answer:?\*?\*?", text, re.IGNORECASE))


# ---------------------------------------------------------------------------
# MCQ detection
# ---------------------------------------------------------------------------
_MCQ_OPTION_RE = re.compile(
    r"\(([A-D])\)\s", re.IGNORECASE
)


def is_mcq_question(user_text: str) -> bool:
    """Detect MCQ by presence of (A)/(B)/(C)/(D) option pattern."""
    matches = _MCQ_OPTION_RE.findall(user_text)
    unique = set(m.upper() for m in matches)
    return len(unique) >= 3  # at least 3 of A/B/C/D


def is_letter_answer(answer: str) -> bool:
    """Check if answer is a bare letter (or set of letters like AB, BCD)."""
    cleaned = re.sub(r"[\s,()\\{}$]", "", answer).strip()
    return bool(cleaned) and all(c in "ABCDabcd" for c in cleaned)


# ---------------------------------------------------------------------------
# 7. Schema Validation
# ---------------------------------------------------------------------------
def check_schema(train_data: list[dict], valid_data: list[dict],
                 sdpo_rl: list[dict], sdpo_eval: list[dict],
                 verbose: bool) -> tuple[list[dict], bool]:
    """Returns (flagged_items, passed)."""
    print(HEADER("\n=== 7. Schema Validation (5% — gate) ==="))
    flags = []
    ok = True

    # SFT data schema
    for label, dataset, path in [
        ("train_full", train_data, TRAIN_FULL),
        ("valid_full", valid_data, VALID_FULL),
    ]:
        for idx, row in enumerate(dataset):
            issues = []
            msgs = row.get("messages")
            if not isinstance(msgs, list) or len(msgs) != 3:
                issues.append(f"messages should be list of 3, got {type(msgs).__name__} len={len(msgs) if isinstance(msgs, list) else '?'}")
            else:
                expected_roles = ["system", "user", "assistant"]
                actual_roles = [m.get("role") for m in msgs]
                if actual_roles != expected_roles:
                    issues.append(f"role order {actual_roles} != {expected_roles}")
                for m in msgs:
                    if not m.get("content", "").strip():
                        issues.append(f"empty content for role={m.get('role')}")

            meta = row.get("metadata", {})
            if label == "train_full":
                for field in ("subject", "source", "question_type"):
                    if field not in meta:
                        issues.append(f"metadata missing '{field}'")

            if issues:
                ok = False
                for issue in issues:
                    flags.append({
                        "index": idx,
                        "check": "schema",
                        "severity": "fix_upstream",
                        "reason": f"{label}:{idx} — {issue}",
                    })
                    if verbose:
                        print(f"  {FAIL(f'{label}:{idx} — {issue}')}")

    # SDPO schema
    for label, dataset in [("rl_prompts", sdpo_rl), ("eval_prompts", sdpo_eval)]:
        required = {"prompt", "ground_truth", "subject"}
        for idx, row in enumerate(dataset):
            missing = required - set(row.keys())
            if missing:
                ok = False
                flags.append({
                    "index": idx,
                    "check": "schema",
                    "severity": "fix_upstream",
                    "reason": f"{label}:{idx} — missing keys: {missing}",
                })
                if verbose:
                    print(f"  {FAIL(f'{label}:{idx} — missing {missing}')}")

    if ok:
        print(f"  {PASS(f'SFT: {len(train_data)} train + {len(valid_data)} valid, SDPO: {len(sdpo_rl)} RL + {len(sdpo_eval)} eval — all valid')}")
    else:
        print(f"  {FAIL(f'{len(flags)} schema issues found — fix format_data.py before other checks')}")
    return flags, ok


# ---------------------------------------------------------------------------
# 1. Semantic & Answer Quality
# ---------------------------------------------------------------------------
def check_semantic_quality(train_data: list[dict], verbose: bool) -> list[dict]:
    print(HEADER("\n=== 1. Semantic & Answer Quality (30%) ==="))
    flags = []

    empty_boxed = 0
    long_boxed = 0
    missing_answer = 0
    mcq_letter_mismatch = 0
    reverse_letter = 0
    coherence_fail = 0
    type_label_mismatch = 0
    system_drift = 0

    for idx, row in enumerate(train_data):
        msgs = row["messages"]
        system_content = msgs[0]["content"]
        user_content = msgs[1]["content"]
        asst_content = msgs[2]["content"]
        meta = row.get("metadata", {})

        # --- System message drift ---
        if system_content != SYSTEM_MESSAGE:
            system_drift += 1
            flags.append({
                "index": idx,
                "check": "system_drift",
                "severity": "fix_upstream",
                "reason": f"System message differs from canonical",
            })

        # --- Boxed answer validation ---
        boxed = extract_boxed(asst_content)
        if boxed is not None:
            stripped = boxed.strip()
            if not stripped or stripped in ("?", "??", "..."):
                empty_boxed += 1
                flags.append({
                    "index": idx,
                    "check": "empty_boxed",
                    "severity": "drop",
                    "reason": f"Empty/placeholder boxed answer: \\boxed{{{boxed}}}",
                })
            elif len(stripped) > 200:
                long_boxed += 1
                flags.append({
                    "index": idx,
                    "check": "long_boxed",
                    "severity": "review",
                    "reason": f"Absurdly long boxed answer ({len(stripped)} chars)",
                })
        else:
            # No \boxed{} — check for Answer: fallback
            if not has_answer_marker(asst_content):
                missing_answer += 1
                flags.append({
                    "index": idx,
                    "check": "missing_answer",
                    "severity": "review",
                    "reason": "No \\boxed{{}} and no 'Answer:' marker",
                })

        # --- MCQ answer consistency ---
        mcq = is_mcq_question(user_content)
        if boxed is not None:
            answer_is_letter = is_letter_answer(boxed)
            if mcq and not answer_is_letter:
                # MCQ but boxed answer is numerical
                mcq_letter_mismatch += 1
                flags.append({
                    "index": idx,
                    "check": "mcq_letter_mismatch",
                    "severity": "review",
                    "reason": f"MCQ question but boxed answer is not a letter: \\boxed{{{boxed[:50]}}}",
                })
            elif not mcq and answer_is_letter and len(boxed.strip()) <= 4:
                reverse_letter += 1
                flags.append({
                    "index": idx,
                    "check": "reverse_letter_mismatch",
                    "severity": "review",
                    "reason": f"Non-MCQ question but boxed a bare letter: \\boxed{{{boxed}}}",
                })

        # --- Solution-answer coherence (numerical only) ---
        if boxed is not None and not is_letter_answer(boxed):
            # Skip complex expressions that are typically assembled from parts
            # across the solution (intervals, piecewise, multi-value answers)
            is_complex = any(cmd in boxed for cmd in (
                r"\begin", r"\left[", r"\left(", r"\text{",
                r"\infty", r"\cases",
            ))
            if not is_complex:
                # Remove the \boxed{} itself to avoid trivially matching
                solution_no_boxed = re.sub(r"\\boxed\{[^}]*\}", "", asst_content)
                norm_solution = normalise_latex(solution_no_boxed)
                boxed_stripped = boxed.strip()
                found = False
                norm_boxed = normalise_latex(boxed)
                # Check fully-normalised
                if norm_boxed and norm_boxed in norm_solution:
                    found = True
                # Check raw form
                elif boxed_stripped and boxed_stripped in solution_no_boxed:
                    found = True
                else:
                    # For multi-value answers (e.g. "3, 7, 23"), check each value
                    parts = re.split(r"[,;]", re.sub(r"\\text\{[^}]*\}", ",", boxed))
                    numeric_parts = []
                    for p in parts:
                        p = p.strip()
                        if not p:
                            continue
                        # Check raw part in solution
                        if p in solution_no_boxed:
                            found = True
                            break
                        # Try numeric extraction
                        try:
                            numeric_parts.append(
                                float(re.sub(r"[^0-9.\-eE]", "", p))
                            )
                        except (ValueError, TypeError):
                            pass
                    if not found and numeric_parts:
                        # Check if all numeric parts appear somewhere
                        def _fmt(n: float) -> str:
                            if math.isinf(n) or math.isnan(n):
                                return ""
                            return str(int(n)) if n == int(n) else str(n)
                        formatted = [_fmt(n) for n in numeric_parts]
                        found = all(
                            s and s in solution_no_boxed for s in formatted
                        ) if formatted else False

                if not found and norm_boxed:
                    coherence_fail += 1
                    flags.append({
                        "index": idx,
                        "check": "coherence_fail",
                        "severity": "review",
                        "reason": f"Boxed answer '{boxed[:60]}' not found in solution text",
                    })

        # --- Question-type label consistency ---
        q_type = meta.get("question_type", "").lower()
        if boxed is not None:
            answer_is_letter = is_letter_answer(boxed)
            if "numerical" in q_type or "numeric" in q_type or "integer" in q_type:
                if answer_is_letter:
                    type_label_mismatch += 1
                    flags.append({
                        "index": idx,
                        "check": "type_label_mismatch",
                        "severity": "review",
                        "reason": f"Type='{meta.get('question_type')}' but boxed answer is letter '{boxed}'",
                    })
            elif "mcq" in q_type:
                if not answer_is_letter and not re.search(r"[A-Da-d]", boxed[:5]):
                    type_label_mismatch += 1
                    flags.append({
                        "index": idx,
                        "check": "type_label_mismatch",
                        "severity": "review",
                        "reason": f"Type='MCQ' but boxed answer is numerical: '{boxed[:50]}'",
                    })

    # Summary
    total = len(train_data)
    print(f"  Boxed answer validation:")
    _report("  Empty/placeholder \\boxed{{}}", empty_boxed, total, threshold=0)
    _report("  Absurdly long \\boxed{{}} (>200 chars)", long_boxed, total, threshold=0)
    _report("  No answer marker at all", missing_answer, total, threshold=0.05)
    print(f"  MCQ consistency:")
    _report("  MCQ question with non-letter answer", mcq_letter_mismatch, total, threshold=0)
    _report("  Non-MCQ with bare letter answer", reverse_letter, total, threshold=0)
    print(f"  Solution coherence:")
    _report("  Boxed answer not in solution text", coherence_fail, total, threshold=0.1)
    print(f"  Label consistency:")
    _report("  Question type vs answer mismatch", type_label_mismatch, total, threshold=0)
    print(f"  System message:")
    _report("  System message drift", system_drift, total, threshold=0)

    return flags


def _report(label: str, count: int, total: int, threshold: float = 0.05):
    pct = count / total if total else 0
    msg = f"{label}: {count}/{total} ({pct:.1%})"
    if count == 0:
        print(f"    {PASS(msg)}")
    elif pct <= threshold:
        print(f"    {WARN(msg)}")
    else:
        print(f"    {FAIL(msg)}")


# ---------------------------------------------------------------------------
# 2 & 5. Coverage & Diversity (includes topic distribution)
# ---------------------------------------------------------------------------
def check_coverage(train_data: list[dict], verbose: bool) -> list[dict]:
    print(HEADER("\n=== 2/5. Coverage & Diversity (15%) ==="))
    flags = []

    # --- Subject × topic cross-tab ---
    subject_counts = collections.Counter()
    source_counts = collections.Counter()
    subject_source = collections.defaultdict(lambda: collections.Counter())
    subject_topic = collections.defaultdict(lambda: collections.Counter())

    topic_keywords = {
        "Physics": JEE_PHYSICS_KEYWORDS,
        "Chemistry": JEE_CHEMISTRY_KEYWORDS,
        "Mathematics": JEE_MATH_KEYWORDS,
    }

    for idx, row in enumerate(train_data):
        meta = row.get("metadata", {})
        subj = meta.get("subject", "Unknown")
        src = meta.get("source", "unknown")
        subject_counts[subj] += 1
        source_counts[src] += 1
        subject_source[subj][src] += 1

        # Classify topic within subject
        user_text = row["messages"][1]["content"].lower()
        keywords = topic_keywords.get(subj, [])
        for kw in keywords:
            if kw in user_text:
                subject_topic[subj][kw] += 1

    total = len(train_data)
    print(f"\n  Subject distribution (n={total}):")
    for subj, count in subject_counts.most_common():
        pct = count / total
        marker = WARN(f"{subj}: {count} ({pct:.1%})") if pct < 0.05 else f"    {subj}: {count} ({pct:.1%})"
        if pct < 0.05:
            print(f"    {marker}")
        else:
            print(f"    {subj}: {count} ({pct:.1%})")

    print(f"\n  Source distribution:")
    for src, count in source_counts.most_common():
        print(f"    {src}: {count} ({count/total:.1%})")

    # Flag single source > 60% of a subject
    print(f"\n  Source diversity per subject:")
    for subj in sorted(subject_source):
        sc = subject_source[subj]
        total_subj = sum(sc.values())
        for src, cnt in sc.most_common(1):
            pct = cnt / total_subj if total_subj else 0
            if pct > 0.8:
                msg = f"{subj}: '{src}' is {pct:.0%} of examples ({cnt}/{total_subj})"
                print(f"    {WARN(msg)}")
                flags.append({
                    "index": -1,
                    "check": "source_dominance",
                    "severity": "review",
                    "reason": msg,
                })
            elif pct > 0.6:
                msg = f"{subj}: '{src}' is {pct:.0%} ({cnt}/{total_subj})"
                print(f"    {WARN(msg)}")
            else:
                print(f"    {subj}: top source '{src}' is {pct:.0%} ({cnt}/{total_subj})")

    # Flag topics with < 2% representation
    print(f"\n  Under-represented topics (<2% within subject):")
    under_rep = 0
    for subj in sorted(subject_topic):
        total_subj = subject_counts[subj]
        for kw, cnt in sorted(subject_topic[subj].items(), key=lambda x: x[1]):
            if cnt / total_subj < 0.02:
                under_rep += 1
                if verbose:
                    print(f"    {subj}/{kw}: {cnt} ({cnt/total_subj:.1%})")
    if under_rep:
        print(f"    {WARN(f'{under_rep} topics below 2% threshold')}")
    else:
        print(f"    {PASS('All topics above 2% threshold')}")

    # --- Exact duplicates ---
    print(f"\n  Exact duplicates (user message hash):")
    hashes = collections.Counter()
    hash_to_indices = collections.defaultdict(list)
    for idx, row in enumerate(train_data):
        h = text_hash(row["messages"][1]["content"])
        hashes[h] += 1
        hash_to_indices[h].append(idx)

    dup_groups = {h: idxs for h, idxs in hash_to_indices.items() if len(idxs) > 1}
    dup_count = sum(len(idxs) - 1 for idxs in dup_groups.values())
    if dup_count:
        print(f"    {WARN(f'{dup_count} exact duplicates in {len(dup_groups)} groups')}")
        for h, idxs in list(dup_groups.items())[:5]:
            flags.append({
                "index": idxs[0],
                "check": "exact_duplicate",
                "severity": "drop",
                "reason": f"Exact duplicate group: indices {idxs}",
            })
            if verbose:
                print(f"      Group: indices {idxs[:5]}{'...' if len(idxs) > 5 else ''}")
    else:
        print(f"    {PASS('No exact duplicates')}")

    # --- Template duplicates ---
    print(f"\n  Template duplicates (structural signature):")
    struct_sigs = collections.defaultdict(list)
    for idx, row in enumerate(train_data):
        meta = row.get("metadata", {})
        subj = meta.get("subject", "Unknown")
        sig = strip_structural(normalise_text(row["messages"][1]["content"]))
        struct_sigs[(subj, sig)].append(idx)

    template_clusters = {k: idxs for k, idxs in struct_sigs.items() if len(idxs) > 8}
    if template_clusters:
        print(f"    {WARN(f'{len(template_clusters)} clusters with >8 identical structural signatures')}")
        for (subj, _sig), idxs in list(template_clusters.items())[:5]:
            flags.append({
                "index": idxs[0],
                "check": "template_duplicate",
                "severity": "review",
                "reason": f"Template cluster ({subj}): {len(idxs)} instances, e.g. indices {idxs[:5]}",
            })
            if verbose:
                print(f"      {subj}: {len(idxs)} instances (e.g. {idxs[:5]})")
    else:
        print(f"    {PASS('No large template clusters (>8)')}")

    # --- Near duplicates (n-gram Jaccard) ---
    print(f"\n  Near duplicates (Jaccard >0.8):")
    # Bucket by length to avoid O(n^2)
    len_buckets = collections.defaultdict(list)
    for idx, row in enumerate(train_data):
        content = row["messages"][1]["content"]
        bucket = len(content) // 100  # 100-char buckets
        len_buckets[bucket].append((idx, content))

    near_dup_pairs = []
    for bucket_key in len_buckets:
        items = len_buckets[bucket_key]
        # Also check adjacent buckets
        adjacent = len_buckets.get(bucket_key + 1, [])
        all_items = items + adjacent
        if len(all_items) > 500:
            # Skip very large buckets to avoid timeout
            continue
        ngrams_cache = {}
        for i, (idx_a, text_a) in enumerate(items):
            if idx_a not in ngrams_cache:
                ngrams_cache[idx_a] = ngram_set(text_a)
            for j in range(i + 1, len(all_items)):
                idx_b, text_b = all_items[j]
                # Length pre-filter
                la, lb = len(text_a), len(text_b)
                if la > 0 and lb > 0:
                    ratio = min(la, lb) / max(la, lb)
                    if ratio < 0.5:
                        continue
                if idx_b not in ngrams_cache:
                    ngrams_cache[idx_b] = ngram_set(text_b)
                j_score = jaccard(ngrams_cache[idx_a], ngrams_cache[idx_b])
                if j_score > 0.8 and idx_a != idx_b:
                    near_dup_pairs.append((idx_a, idx_b, j_score))

    if near_dup_pairs:
        print(f"    {WARN(f'{len(near_dup_pairs)} near-duplicate pairs found')}")
        for a, b, score in near_dup_pairs[:5]:
            flags.append({
                "index": a,
                "check": "near_duplicate",
                "severity": "review",
                "reason": f"Near duplicate pair ({a}, {b}) Jaccard={score:.3f}",
            })
            if verbose:
                print(f"      ({a}, {b}) Jaccard={score:.3f}")
    else:
        print(f"    {PASS('No near duplicates')}")

    return flags


# ---------------------------------------------------------------------------
# 3. Contamination
# ---------------------------------------------------------------------------
def check_contamination(train_data: list[dict], valid_data: list[dict],
                        sdpo_eval: list[dict], verbose: bool) -> list[dict]:
    print(HEADER("\n=== 3. Contamination (25%) ==="))
    flags = []

    def get_user_text(row: dict) -> str:
        if "messages" in row:
            return row["messages"][1]["content"]
        return row.get("prompt", row.get("question", ""))

    train_texts = [(i, get_user_text(r)) for i, r in enumerate(train_data)]
    valid_texts = [(i, get_user_text(r)) for i, r in enumerate(valid_data)]
    eval_texts = [(i, get_user_text(r)) for i, r in enumerate(sdpo_eval)]

    # --- Internal: train vs valid ---
    print(f"\n  Internal overlap (train vs valid):")
    train_hashes = {text_hash(t): idx for idx, t in train_texts}
    valid_hashes = {text_hash(t): idx for idx, t in valid_texts}
    exact_overlap = set(train_hashes.keys()) & set(valid_hashes.keys())
    if exact_overlap:
        print(f"    {FAIL(f'{len(exact_overlap)} exact train/valid overlaps')}")
        for h in list(exact_overlap)[:5]:
            ti, vi = train_hashes[h], valid_hashes[h]
            flags.append({
                "index": ti,
                "check": "train_valid_overlap",
                "severity": "drop",
                "reason": f"Exact overlap: train[{ti}] == valid[{vi}]",
            })
    else:
        print(f"    {PASS('No exact train/valid overlap')}")

    # Train vs SDPO eval
    eval_hashes = {text_hash(t): idx for idx, t in eval_texts}
    eval_overlap = set(train_hashes.keys()) & set(eval_hashes.keys())
    if eval_overlap:
        print(f"    {FAIL(f'{len(eval_overlap)} exact train/eval_prompts overlaps')}")
        for h in list(eval_overlap)[:5]:
            flags.append({
                "index": train_hashes[h],
                "check": "train_eval_overlap",
                "severity": "drop",
                "reason": f"Exact overlap: train[{train_hashes[h]}] == eval[{eval_hashes[h]}]",
            })
    else:
        print(f"    {PASS('No exact train/eval overlap')}")

    # Fuzzy: valid vs train
    print(f"\n  Fuzzy overlap (valid vs train, threshold=0.85):")
    fuzzy_matches = 0
    for vi, vtext in valid_texts:
        vlen = len(vtext)
        if vlen < 50:
            continue
        for ti, ttext in train_texts:
            # Length pre-filter (>30% overlap in length)
            tlen = len(ttext)
            if min(vlen, tlen) / max(vlen, tlen) < 0.3:
                continue
            ratio = difflib.SequenceMatcher(None, normalise_text(vtext), normalise_text(ttext)).ratio()
            if ratio >= 0.85:
                fuzzy_matches += 1
                flags.append({
                    "index": ti,
                    "check": "fuzzy_train_valid",
                    "severity": "drop",
                    "reason": f"Fuzzy match ({ratio:.2f}): train[{ti}] ~ valid[{vi}]",
                })
                if fuzzy_matches >= 50:
                    break
        if fuzzy_matches >= 50:
            break

    if fuzzy_matches:
        print(f"    {WARN(f'{fuzzy_matches} fuzzy matches found')}")
    else:
        print(f"    {PASS('No fuzzy train/valid overlap')}")

    # --- Benchmark contamination ---
    print(f"\n  Benchmark contamination:")
    benchmark_questions = []
    for name, path in BENCHMARK_PATHS:
        if path.suffix == ".jsonl":
            rows = load_jsonl(path)
            for r in rows:
                q = r.get("question", r.get("prompt", r.get("text", "")))
                if q:
                    benchmark_questions.append((name, q))
        elif path.is_dir():
            rows = load_hf_dataset(path)
            for r in rows:
                q = r.get("Question Text", r.get("question", r.get("prompt", "")))
                if q:
                    benchmark_questions.append((name, q))

    if not benchmark_questions:
        print(f"    {INFO('No benchmark data found to check')}")
    else:
        print(f"    Loaded {len(benchmark_questions)} benchmark questions")
        bench_hashes = {}
        for bname, bq in benchmark_questions:
            h = text_hash(bq)
            bench_hashes[h] = (bname, bq)

        exact_bench = 0
        fuzzy_bench = 0
        for ti, ttext in train_texts:
            th = text_hash(ttext)
            if th in bench_hashes:
                bname, _ = bench_hashes[th]
                exact_bench += 1
                flags.append({
                    "index": ti,
                    "check": "benchmark_exact",
                    "severity": "drop",
                    "reason": f"Exact match with {bname} benchmark",
                })

        # Fuzzy benchmark check (sample to avoid timeout)
        sample_size = min(len(benchmark_questions), 200)
        bench_sample = random.sample(benchmark_questions, sample_size)
        for bname, bq in bench_sample:
            bq_norm = normalise_text(bq)
            blen = len(bq)
            if blen < 50:
                continue
            for ti, ttext in train_texts:
                tlen = len(ttext)
                if min(blen, tlen) / max(blen, tlen) < 0.3:
                    continue
                ratio = difflib.SequenceMatcher(
                    None, bq_norm, normalise_text(ttext)
                ).ratio()
                if ratio >= 0.85:
                    fuzzy_bench += 1
                    flags.append({
                        "index": ti,
                        "check": "benchmark_fuzzy",
                        "severity": "drop",
                        "reason": f"Fuzzy match ({ratio:.2f}) with {bname} benchmark",
                    })
                    break

        _report("    Exact benchmark matches", exact_bench, total=len(train_data), threshold=0)
        if fuzzy_bench:
            print(f"    {WARN(f'{fuzzy_bench} fuzzy benchmark matches')}")
        else:
            print(f"    {PASS(f'No fuzzy benchmark matches (sampled {sample_size})')}")

    return flags


# ---------------------------------------------------------------------------
# 4. Token Length & Reasoning Quality
# ---------------------------------------------------------------------------
def check_token_length(train_data: list[dict], skip_tokenize: bool,
                       verbose: bool) -> list[dict]:
    print(HEADER("\n=== 4. Token Length & Reasoning Quality (15%) ==="))
    flags = []

    if skip_tokenize:
        print(f"  {INFO('Skipped (--skip-tokenize)')}")
        return flags

    # Try Qwen3 tokenizer, fallback to tiktoken
    tokenizer = None
    tokenizer_name = None
    try:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            "Qwen/Qwen3-8B", trust_remote_code=True
        )
        tokenizer_name = "Qwen3-8B"
    except Exception:
        try:
            import tiktoken
            tokenizer = tiktoken.get_encoding("cl100k_base")
            tokenizer_name = "tiktoken/cl100k_base"
        except ImportError:
            print(f"  {WARN('No tokenizer available — install transformers or tiktoken')}")
            return flags

    print(f"  Tokenizer: {tokenizer_name}")

    def count_tokens(text: str) -> int:
        if hasattr(tokenizer, "encode"):
            return len(tokenizer.encode(text))
        return len(tokenizer.encode(text))

    # Collect per-message token counts
    system_lens = []
    user_lens = []
    asst_lens = []
    total_lens = []

    for row in train_data:
        msgs = row["messages"]
        sl = count_tokens(msgs[0]["content"])
        ul = count_tokens(msgs[1]["content"])
        al = count_tokens(msgs[2]["content"])
        system_lens.append(sl)
        user_lens.append(ul)
        asst_lens.append(al)
        total_lens.append(sl + ul + al)

    import numpy as np
    asst_arr = np.array(asst_lens)
    total_arr = np.array(total_lens)

    print(f"\n  Assistant token stats (n={len(asst_arr)}):")
    for label, arr in [("Assistant", asst_arr)]:
        print(f"    mean={arr.mean():.0f}  median={np.median(arr):.0f}  "
              f"std={arr.std():.0f}  min={arr.min()}  max={arr.max()}")
        print(f"    p5={np.percentile(arr,5):.0f}  p25={np.percentile(arr,25):.0f}  "
              f"p75={np.percentile(arr,75):.0f}  p95={np.percentile(arr,95):.0f}")

    # Histogram
    bins = [0, 50, 100, 200, 400, 800, float("inf")]
    bin_labels = ["<50", "50-100", "100-200", "200-400", "400-800", "800+"]
    hist = collections.Counter()
    for l in asst_lens:
        for i in range(len(bins) - 1):
            if bins[i] <= l < bins[i + 1]:
                hist[bin_labels[i]] += 1
                break

    print(f"\n  Assistant token histogram:")
    for label in bin_labels:
        cnt = hist[label]
        pct = cnt / len(asst_lens) if asst_lens else 0
        bar = "#" * int(pct * 40)
        print(f"    {label:>8s}: {cnt:5d} ({pct:5.1%}) {bar}")

    # --- Short-answer distribution per subject ---
    print(f"\n  Short-answer distribution (<100 tokens, per subject):")
    subject_short = collections.defaultdict(int)
    subject_total = collections.defaultdict(int)
    for idx, row in enumerate(train_data):
        subj = row.get("metadata", {}).get("subject", "Unknown")
        subject_total[subj] += 1
        if asst_lens[idx] < 100:
            subject_short[subj] += 1

    for subj in sorted(subject_total):
        pct = subject_short[subj] / subject_total[subj] if subject_total[subj] else 0
        msg = f"{subj}: {subject_short[subj]}/{subject_total[subj]} ({pct:.0%}) short"
        if pct > 0.4:
            print(f"    {FAIL(msg)}")
            flags.append({
                "index": -1,
                "check": "short_answer_distribution",
                "severity": "review",
                "reason": f"{subj}: {pct:.0%} of examples have <100 token assistant responses",
            })
        elif pct > 0.2:
            print(f"    {WARN(msg)}")
        else:
            print(f"    {PASS(msg)}")

    # --- Overflow detection ---
    SFT_MAX = 8192
    SDPO_MAX = 2048
    sft_overflow = sum(1 for t in total_lens if t > SFT_MAX)
    sdpo_overflow = sum(1 for t in total_lens if t > SDPO_MAX)

    print(f"\n  Overflow detection:")
    _report(f"  Exceeding SFT max_seq={SFT_MAX}", sft_overflow, len(total_lens), threshold=0.1)
    _report(f"  Exceeding SDPO max_length={SDPO_MAX}", sdpo_overflow, len(total_lens), threshold=0.01)

    for idx, tl in enumerate(total_lens):
        if tl > SDPO_MAX:
            flags.append({
                "index": idx,
                "check": "sdpo_overflow",
                "severity": "review",
                "reason": f"Total tokens ({tl}) exceeds SDPO max_length={SDPO_MAX}",
            })

    return flags


# ---------------------------------------------------------------------------
# 6. LaTeX Validation
# ---------------------------------------------------------------------------
# Broken commands — matched with regex word boundaries to avoid false positives
# (e.g. \tex should NOT match inside \text)
BROKEN_COMMANDS_RE = [
    (re.compile(r"\\frc(?![a-zA-Z])"), r"\frac"),
    (re.compile(r"\\sqr(?![a-zA-Z])"), r"\sqrt"),
    (re.compile(r"\\iteint(?![a-zA-Z])"), r"\int"),
    (re.compile(r"\\limt(?![a-zA-Z])"), r"\lim"),
    (re.compile(r"\\tex(?![a-zA-Z])"), r"\text"),
    (re.compile(r"\\mathr(?![a-zA-Z])"), r"\mathrm"),
]

MOJIBAKE_PATTERNS = ["\ufffd", "Ã¤", "â€™", "â€œ", "â€\x9d", "\x00"]


def check_latex(train_data: list[dict], verbose: bool) -> list[dict]:
    print(HEADER("\n=== 6. LaTeX Validation (10%) ==="))
    flags = []

    unbalanced_dollar = 0
    unbalanced_braces = 0
    unmatched_env = 0
    broken_cmd = 0
    double_escaped = 0
    mojibake = 0
    cjk_flag = 0

    for idx, row in enumerate(train_data):
        for msg in row["messages"]:
            text = msg["content"]
            role = msg["role"]

            # --- Balanced $ and $$ ---
            # Count $ not preceded by \
            dollars = re.findall(r"(?<!\\)\$", text)
            # Filter out $$ (display mode) — count $$ as pairs
            dd_count = text.count("$$")
            single_count = len(dollars) - 2 * dd_count
            if single_count % 2 != 0:
                unbalanced_dollar += 1
                if role == "assistant":  # only flag assistant
                    flags.append({
                        "index": idx,
                        "check": "unbalanced_dollar",
                        "severity": "fix_upstream",
                        "reason": f"Unbalanced $ delimiters in {role} message",
                    })
                break  # one flag per example

            # --- Balanced braces in \boxed{} ---
            if "\\boxed{" in text:
                boxed = extract_boxed(text)
                if boxed is not None:
                    # Check if braces are balanced within boxed content
                    depth = 0
                    ok = True
                    for ch in boxed:
                        if ch == "{":
                            depth += 1
                        elif ch == "}":
                            depth -= 1
                        if depth < 0:
                            ok = False
                            break
                    if not ok or depth != 0:
                        unbalanced_braces += 1
                        flags.append({
                            "index": idx,
                            "check": "unbalanced_boxed_braces",
                            "severity": "fix_upstream",
                            "reason": f"Unbalanced braces inside \\boxed{{}}",
                        })

            # --- Matched \begin{} / \end{} ---
            begins = re.findall(r"\\begin\{(\w+)\}", text)
            ends = re.findall(r"\\end\{(\w+)\}", text)
            if collections.Counter(begins) != collections.Counter(ends):
                unmatched_env += 1
                flags.append({
                    "index": idx,
                    "check": "unmatched_environment",
                    "severity": "fix_upstream",
                    "reason": f"Unmatched \\begin/\\end: begins={dict(collections.Counter(begins))}, ends={dict(collections.Counter(ends))}",
                })

            # --- Broken commands ---
            for pattern, good in BROKEN_COMMANDS_RE:
                if pattern.search(text):
                    broken_cmd += 1
                    flags.append({
                        "index": idx,
                        "check": "broken_latex_command",
                        "severity": "fix_upstream",
                        "reason": f"Broken LaTeX command '{pattern.pattern}' (should be '{good}')",
                    })
                    break

            # --- Double-escaped backslashes ---
            if re.search(r"\\\\\\\\(frac|boxed|sqrt|text|mathrm|begin|end)", text):
                double_escaped += 1
                flags.append({
                    "index": idx,
                    "check": "double_escaped",
                    "severity": "fix_upstream",
                    "reason": "Double-escaped backslashes (multiple JSON serialization layers)",
                })

            # --- Mojibake ---
            for pattern in MOJIBAKE_PATTERNS:
                if pattern in text:
                    mojibake += 1
                    flags.append({
                        "index": idx,
                        "check": "mojibake",
                        "severity": "fix_upstream",
                        "reason": f"Mojibake detected: {repr(pattern)}",
                    })
                    break

            # --- CJK ratio ---
            if text:
                cjk_chars = sum(1 for c in text if "\u4e00" <= c <= "\u9fff"
                                or "\u3040" <= c <= "\u30ff"
                                or "\uac00" <= c <= "\ud7af")
                if len(text) > 0 and cjk_chars / len(text) > 0.1:
                    cjk_flag += 1
                    flags.append({
                        "index": idx,
                        "check": "cjk_content",
                        "severity": "review",
                        "reason": f"CJK ratio {cjk_chars/len(text):.0%} (>10%) — non-English content",
                    })

    total = len(train_data)
    _report("  Unbalanced $ delimiters", unbalanced_dollar, total, threshold=0.02)
    _report("  Unbalanced braces in \\boxed{{}}", unbalanced_braces, total, threshold=0)
    _report("  Unmatched \\begin/\\end", unmatched_env, total, threshold=0.01)
    _report("  Broken LaTeX commands", broken_cmd, total, threshold=0)
    _report("  Double-escaped backslashes", double_escaped, total, threshold=0)
    _report("  Mojibake / null bytes", mojibake, total, threshold=0)
    _report("  CJK content >10%", cjk_flag, total, threshold=0)

    return flags


# ---------------------------------------------------------------------------
# 8. Raw Dataset Inventory
# ---------------------------------------------------------------------------
RAW_DATASETS = [
    ("jeebench", RAW_DIR / "jeebench"),
    ("kaggle_jee", RAW_DIR / "kaggle_jee"),
    ("kaggle_iitjee", RAW_DIR / "kaggle_iitjee"),
    ("numinamath", RAW_DIR / "numinamath"),
    ("sciinstruct", RAW_DIR / "sciinstruct"),
    ("jee_mains_2025", RAW_DIR / "jee" / "jee_mains_2025"),
    ("jee_main_2025_math", RAW_DIR / "jee" / "jee_main_2025_math"),
    ("jee_neet_benchmark", RAW_DIR / "jee" / "jee_neet_benchmark_reja1"),
    ("kaggle_aimo_olympiad", RAW_DIR / "kaggle_aimo_olympiad"),
    ("kaggle_math_olympiad", RAW_DIR / "kaggle_math_olympiad"),
    ("kaggle_ncert", RAW_DIR / "kaggle_ncert"),
    ("kaggle_ncert_md", RAW_DIR / "kaggle_ncert_md"),
    ("chemistry", RAW_DIR / "chemistry"),
    ("physics", RAW_DIR / "physics"),
    ("math", RAW_DIR / "math"),
    ("ncert", RAW_DIR / "ncert"),
    ("science", RAW_DIR / "science"),
]


def check_raw_inventory(skip_raw: bool, verbose: bool) -> list[dict]:
    print(HEADER("\n=== 8. Raw Dataset Inventory (not scored) ==="))
    flags = []

    if skip_raw:
        print(f"  {INFO('Skipped (--skip-raw)')}")
        return flags

    for name, path in RAW_DATASETS:
        if not path.exists():
            print(f"  {FAIL(f'{name}: directory not found at {path}')}")
            flags.append({
                "index": -1,
                "check": "raw_missing",
                "severity": "review",
                "reason": f"Raw dataset '{name}' not found at {path}",
            })
            continue

        # Count data files
        data_files = list(path.rglob("*.jsonl")) + list(path.rglob("*.json")) + \
                     list(path.rglob("*.csv")) + list(path.rglob("*.parquet")) + \
                     list(path.rglob("*.arrow"))
        total_size = sum(f.stat().st_size for f in data_files if f.exists())

        # Count rows in jsonl/csv files
        row_count = 0
        for f in data_files:
            if f.suffix == ".jsonl":
                try:
                    with open(f) as fh:
                        row_count += sum(1 for line in fh if line.strip())
                except Exception:
                    pass
            elif f.suffix == ".csv":
                try:
                    with open(f) as fh:
                        row_count += sum(1 for _ in fh) - 1  # minus header
                except Exception:
                    pass

        size_mb = total_size / (1024 * 1024)
        if len(data_files) == 0 or total_size == 0:
            print(f"  {WARN(f'{name}: empty (0 data files)')}")
            flags.append({
                "index": -1,
                "check": "raw_empty",
                "severity": "review",
                "reason": f"Raw dataset '{name}' is empty",
            })
        else:
            files_desc = f"{len(data_files)} files, {size_mb:.1f}MB"
            if row_count:
                files_desc += f", ~{row_count} rows"
            print(f"  {PASS(f'{name}: {files_desc}')}")

    return flags


# ---------------------------------------------------------------------------
# Manual Review Sample
# ---------------------------------------------------------------------------
def generate_sample(train_data: list[dict], n: int):
    if n <= 0:
        return

    print(HEADER(f"\n=== Generating Manual Review Sample (n={n}) ==="))

    # Stratified by subject
    by_subject = collections.defaultdict(list)
    for idx, row in enumerate(train_data):
        subj = row.get("metadata", {}).get("subject", "Unknown")
        by_subject[subj].append((idx, row))

    subjects = ["Physics", "Chemistry", "Mathematics"]
    per_subject = max(1, n // len(subjects))
    remainder = n - per_subject * len(subjects)

    sampled = []
    for subj in subjects:
        pool = by_subject.get(subj, [])
        k = min(per_subject, len(pool))
        if subj == subjects[-1]:
            k = min(k + max(0, remainder), len(pool))
        sampled.extend(random.sample(pool, k))

    # Fill remainder from any subject if needed
    while len(sampled) < n:
        all_remaining = [(i, r) for s in by_subject.values() for i, r in s
                         if (i, r) not in sampled]
        if not all_remaining:
            break
        sampled.append(random.choice(all_remaining))

    random.shuffle(sampled)

    lines = [f"# Quality Review Sample ({len(sampled)} examples)\n",
             f"Generated: {__import__('datetime').datetime.now().isoformat()}\n"]

    for i, (idx, row) in enumerate(sampled, 1):
        meta = row.get("metadata", {})
        user = row["messages"][1]["content"]
        asst = row["messages"][2]["content"]

        lines.append(f"\n---\n\n## Example {i} (JSONL index: {idx})\n")
        lines.append(f"- **Subject:** {meta.get('subject', '?')}")
        lines.append(f"- **Source:** {meta.get('source', '?')}")
        lines.append(f"- **Type:** {meta.get('question_type', '?')}\n")
        lines.append(f"### Question\n\n{user}\n")
        lines.append(f"### Solution (first 500 chars)\n\n{asst[:500]}\n")
        if len(asst) > 500:
            lines.append(f"\n*...({len(asst) - 500} more chars)*\n")

    SAMPLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SAMPLE_PATH.write_text("\n".join(lines))
    print(f"  {PASS(f'Saved {len(sampled)} examples to {SAMPLE_PATH}')}")


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------
WEIGHTS = {
    "semantic": 0.30,
    "contamination": 0.25,
    "token_length": 0.15,
    "coverage": 0.15,
    "latex": 0.10,
    "schema": 0.05,
}


def compute_scores(all_flags: dict[str, list[dict]], total: int,
                   schema_passed: bool) -> dict:
    """Compute per-category and overall scores."""
    scores = {}

    for category, weight in WEIGHTS.items():
        cat_flags = all_flags.get(category, [])
        drop_count = sum(1 for f in cat_flags if f["severity"] == "drop")
        review_count = sum(1 for f in cat_flags if f["severity"] == "review")
        fix_count = sum(1 for f in cat_flags if f["severity"] == "fix_upstream")

        if category == "schema":
            score = 1.0 if schema_passed else 0.0
        else:
            # Penalty: drops count fully, reviews half, fixes quarter
            penalty_total = drop_count + review_count * 0.5 + fix_count * 0.25
            # Score is 1 - (penalty / total), clamped to [0, 1]
            score = max(0.0, 1.0 - (penalty_total / total)) if total else 0.0

        scores[category] = {
            "score": round(score, 3),
            "weight": weight,
            "weighted": round(score * weight, 3),
            "drops": drop_count,
            "reviews": review_count,
            "fixes": fix_count,
        }

    overall = sum(s["weighted"] for s in scores.values())
    return {"categories": scores, "overall": round(overall, 3)}


def print_scores(scores: dict):
    print(HEADER("\n=== Overall Quality Score ===\n"))
    for cat, data in scores["categories"].items():
        s = data["score"]
        w = data["weight"]
        ws = data["weighted"]
        detail = f"drops={data['drops']}, reviews={data['reviews']}, fixes={data['fixes']}"
        if s >= 0.9:
            grade = PASS(f"{s:.1%}")
        elif s >= 0.7:
            grade = WARN(f"{s:.1%}")
        else:
            grade = FAIL(f"{s:.1%}")
        print(f"  {cat:20s}  {grade}  (weight={w:.0%}, weighted={ws:.3f})  [{detail}]")

    overall = scores["overall"]
    if overall >= 0.85:
        print(f"\n  {'Overall':20s}  {PASS(f'{overall:.1%}')}")
    elif overall >= 0.7:
        print(f"\n  {'Overall':20s}  {WARN(f'{overall:.1%}')}")
    else:
        print(f"\n  {'Overall':20s}  {FAIL(f'{overall:.1%}')}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Data quality checks for JEE fine-tuning")
    parser.add_argument("--skip-tokenize", action="store_true",
                        help="Skip token counting (faster)")
    parser.add_argument("--skip-raw", action="store_true",
                        help="Skip raw dataset inventory")
    parser.add_argument("--sample", type=int, default=0,
                        help="Generate N manual review examples (default: 0)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose output")
    args = parser.parse_args()

    print("=" * 65)
    print("  JEE Fine-Tuning Data Quality Check")
    print("=" * 65)

    # Load data
    print(f"\nLoading data...")
    train_data = load_jsonl(TRAIN_FULL)
    valid_data = load_jsonl(VALID_FULL)
    sdpo_rl = load_jsonl(SDPO_RL)
    sdpo_eval = load_jsonl(SDPO_EVAL)

    print(f"  train_full:    {len(train_data)} examples")
    print(f"  valid_full:    {len(valid_data)} examples")
    print(f"  sdpo/rl:       {len(sdpo_rl)} prompts")
    print(f"  sdpo/eval:     {len(sdpo_eval)} prompts")

    if not train_data:
        print(FAIL("\nNo training data found. Run format_data.py first."))
        sys.exit(1)

    all_flags: dict[str, list[dict]] = {}

    # 7. Schema (gate)
    schema_flags, schema_ok = check_schema(
        train_data, valid_data, sdpo_rl, sdpo_eval, args.verbose
    )
    all_flags["schema"] = schema_flags

    if not schema_ok:
        print(FAIL("\nSchema validation failed — skipping remaining checks."))
        print("Fix format_data.py and re-run.")
        # Still write partial report
        scores = compute_scores(all_flags, len(train_data), schema_ok)
        _write_report(all_flags, scores, len(train_data))
        print_scores(scores)
        sys.exit(1)

    # 1. Semantic & Answer Quality
    all_flags["semantic"] = check_semantic_quality(train_data, args.verbose)

    # 2/5. Coverage & Diversity
    all_flags["coverage"] = check_coverage(train_data, args.verbose)

    # 3. Contamination
    all_flags["contamination"] = check_contamination(
        train_data, valid_data, sdpo_eval, args.verbose
    )

    # 4. Token Length
    all_flags["token_length"] = check_token_length(
        train_data, args.skip_tokenize, args.verbose
    )

    # 6. LaTeX
    all_flags["latex"] = check_latex(train_data, args.verbose)

    # 8. Raw Inventory
    raw_flags = check_raw_inventory(args.skip_raw, args.verbose)
    # Not scored, but include in report
    all_flags["raw_inventory"] = raw_flags

    # Sample
    if args.sample > 0:
        generate_sample(train_data, args.sample)

    # Scores
    scores = compute_scores(all_flags, len(train_data), schema_ok)
    print_scores(scores)

    # Write report
    _write_report(all_flags, scores, len(train_data))

    total_flags = sum(len(v) for v in all_flags.values())
    print(f"\n  Total flags: {total_flags}")
    print(f"  Report: {REPORT_PATH}")
    if args.sample > 0:
        print(f"  Sample: {SAMPLE_PATH}")


def _write_report(all_flags: dict, scores: dict, total: int):
    report = {
        "total_examples": total,
        "scores": scores,
        "flags_by_category": {
            cat: flags for cat, flags in all_flags.items()
        },
        "flag_counts": {
            cat: {
                "total": len(flags),
                "drop": sum(1 for f in flags if f.get("severity") == "drop"),
                "review": sum(1 for f in flags if f.get("severity") == "review"),
                "fix_upstream": sum(1 for f in flags if f.get("severity") == "fix_upstream"),
            }
            for cat, flags in all_flags.items()
        },
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
