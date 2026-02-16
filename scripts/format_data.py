#!/usr/bin/env python3
"""
Phase 1c: Format data for MLX-LM SFT training.

Reads CoT-augmented datasets and raw datasets, filters for JEE-relevant content,
applies LaTeX cleaning and MCQ fixes, and outputs train.jsonl / valid.jsonl
in mlx-lm chat format.

New sources: PhysicsEval, PhysReason, SciBench, NCERT, entrance-exam-dataset,
ChemistryQA, GPQA Diamond (via opus queue).

Usage:
    python scripts/format_data.py                # full pipeline
    python scripts/format_data.py --merge-opus    # merge Opus solutions into train/valid
"""

import argparse
import collections
import difflib
import json
import random
import re
import sys
from pathlib import Path

from tqdm import tqdm

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
COT_DIR = DATA_DIR / "cot"

SYSTEM_MESSAGE = (
    "You are an expert IIT JEE tutor. Solve problems step-by-step using LaTeX notation. "
    "Show all work clearly and arrive at the final answer."
)

# Keywords for filtering JEE-relevant content from large datasets
JEE_PHYSICS_KEYWORDS = [
    "mechanics", "kinematics", "dynamics", "newton", "friction", "energy",
    "momentum", "rotation", "gravitation", "oscillation", "wave", "sound",
    "thermodynamics", "heat", "entropy", "carnot", "optics", "lens", "mirror",
    "refraction", "diffraction", "interference", "electrostatics", "coulomb",
    "electric field", "potential", "capacitor", "current", "resistance",
    "magnetic", "induction", "electromagnetic", "photoelectric", "nuclear",
    "radioactive", "semiconductor", "projectile", "torque", "angular",
]

JEE_CHEMISTRY_KEYWORDS = [
    "organic", "inorganic", "physical chemistry", "equilibrium", "kinetics",
    "electrochemistry", "thermochemistry", "solution", "mole", "stoichiometry",
    "periodic table", "chemical bond", "hybridization", "molecular orbital",
    "coordination compound", "isomer", "stereochemistry", "reaction mechanism",
    "aldehyde", "ketone", "carboxylic", "amine", "alcohol", "ether", "alkene",
    "alkyne", "aromatic", "polymer", "biomolecule", "redox", "galvanic",
    "nernst", "ph", "buffer", "solubility", "salt", "acid", "base",
]

JEE_MATH_KEYWORDS = [
    "algebra", "quadratic", "polynomial", "complex number", "matrix",
    "determinant", "permutation", "combination", "binomial", "sequence",
    "series", "limit", "continuity", "derivative", "differentiation",
    "integration", "integral", "differential equation", "coordinate geometry",
    "conic", "parabola", "ellipse", "hyperbola", "circle", "straight line",
    "vector", "3d geometry", "three dimensional", "probability", "statistics",
    "trigonometry", "triangle", "logarithm", "function", "inverse function",
    "maxima", "minima", "area under", "definite integral",
]

ALL_JEE_KEYWORDS = JEE_PHYSICS_KEYWORDS + JEE_CHEMISTRY_KEYWORDS + JEE_MATH_KEYWORDS

TRAIN_SPLIT = 0.9


# ---------------------------------------------------------------------------
# LaTeX cleaning (Change 6)
# ---------------------------------------------------------------------------
MOJIBAKE_MAP = {
    # Greek letters
    'Î±': 'α', 'Î²': 'β', 'Î³': 'γ', 'Î´': 'δ', 'Îµ': 'ε',
    'Î·': 'η', 'Î¸': 'θ', 'Î¹': 'ι', 'Î»': 'λ', 'Î¼': 'μ',
    'Î½': 'ν', 'Ï': 'ρ',
    # Degree / superscripts
    'Â°': '°', 'Â¹': '¹', 'Â²': '²', 'Â³': '³',
    # Accented characters
    'Ã©': 'é', 'Ã¡': 'á', 'Ã\xad': 'í',
    # Special
    'Â´': '´',
}


def clean_latex(text: str) -> str | None:
    """Clean LaTeX issues in text. Returns None if text should be skipped."""
    # Normalize frac variants
    text = re.sub(r'\\[dt]frac', r'\\frac', text)
    # Fix double-escaped backslashes
    text = re.sub(r'\\\\(frac|boxed|sqrt|text|mathrm|begin|end|left|right)', r'\\\1', text)
    # Replace mojibake with correct characters
    for mojibake, correct in MOJIBAKE_MAP.items():
        text = text.replace(mojibake, correct)
    # Strip null bytes and remaining mojibake
    text = text.replace('\x00', '')
    for pattern in ['\ufffd', '\u00c3\u00a4', '\u00e2\u0080\u0099', '\u00e2\u0080\u009c', '\u00e2\u0080\u009d']:
        text = text.replace(pattern, '')
    # Check CJK ratio
    if text:
        cjk = sum(1 for c in text if '\u4e00' <= c <= '\u9fff' or '\u3040' <= c <= '\u30ff' or '\uac00' <= c <= '\ud7af')
        if cjk / len(text) > 0.1:
            return None
    return text


def is_valid_entry(entry: dict) -> bool:
    """Check if entry has valid LaTeX structure."""
    text = entry["messages"][2]["content"]  # assistant
    # Check balanced braces in \boxed{}
    if '\\boxed{' in text:
        depth = 0
        in_boxed = False
        for i, ch in enumerate(text):
            if text[i:i+7] == '\\boxed{':
                in_boxed = True
            if in_boxed:
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                if depth == 0:
                    in_boxed = False
                if depth < 0:
                    return False
    # Check matched \begin/\end
    begins = re.findall(r'\\begin\{(\w+)\}', text)
    ends = re.findall(r'\\end\{(\w+)\}', text)
    if collections.Counter(begins) != collections.Counter(ends):
        return False
    return True


# ---------------------------------------------------------------------------
# MCQ answer fix (Change 4)
# ---------------------------------------------------------------------------
def _extract_boxed(text: str) -> str:
    """Extract content of the last \\boxed{...}, handling nested braces."""
    idx = text.rfind('\\boxed{')
    if idx == -1:
        return ""
    depth = 0
    start = idx + 7  # len('\\boxed{')
    for i in range(start, len(text)):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            if depth == 0:
                return text[start:i]
            depth -= 1
    return ""


def _extract_option_map(user_content: str) -> dict[str, str]:
    """Extract option map {A: 'text', B: 'text', ...} from user message."""
    option_map = {}
    for m in re.finditer(r'\(([A-D])\)\s*(.+?)(?=\s*\([A-D]\)|\s*$|\n)', user_content, re.IGNORECASE):
        letter = m.group(1).upper()
        text = m.group(2).strip()
        option_map[letter] = text
    return option_map


def fix_mcq_answer(user_content: str, assistant_content: str) -> str:
    """If user has MCQ options but boxed answer is numeric, try to fix to letter."""
    # Check if MCQ
    mcq_opts = re.findall(r'\(([A-D])\)\s', user_content, re.IGNORECASE)
    if len(set(m.upper() for m in mcq_opts)) < 3:
        return assistant_content  # Not MCQ
    # Check if boxed answer is numeric
    boxed_match = re.search(r'\\boxed\{([^}]+)\}', assistant_content)
    if not boxed_match:
        return assistant_content
    boxed = boxed_match.group(1).strip()
    if re.match(r'^[A-Da-d]$', boxed):
        return assistant_content  # Already a letter
    # Search for expanded letter patterns in solution
    letter_match = re.search(
        r'(?:answer|option|correct|choose)\s*(?:is\s*)?'
        r'(?:the\s+)?(?:correct\s+)?(?:option\s+)?'
        r'\(?([A-D])\)?'
        r'|'
        r'\(?([A-D])\)?\s+is\s+(?:the\s+)?correct',
        assistant_content, re.IGNORECASE,
    )
    if letter_match:
        letter = (letter_match.group(1) or letter_match.group(2)).upper()
        return assistant_content.replace(f'\\boxed{{{boxed}}}', f'\\boxed{{{letter}}}')
    # Match boxed numeric value against MCQ option text content
    option_map = _extract_option_map(user_content)
    if option_map:
        boxed_norm = boxed.strip().replace(' ', '')
        for letter, text in option_map.items():
            text_norm = text.strip().replace(' ', '')
            # Check if boxed value matches the option text
            if boxed_norm == text_norm or boxed_norm in text_norm or text_norm in boxed_norm:
                return assistant_content.replace(f'\\boxed{{{boxed}}}', f'\\boxed{{{letter}}}')
    return assistant_content  # Can't fix, leave as-is


# ---------------------------------------------------------------------------
# Semantic quality fixes (Plan v4)
# ---------------------------------------------------------------------------
def fix_coherence_answer(assistant_content: str) -> str:
    """If boxed answer doesn't appear in solution text, insert bridging sentence."""
    boxed = _extract_boxed(assistant_content)
    if not boxed or len(boxed) > 80:
        return assistant_content  # Empty or too long to fix

    # Remove all \boxed{...} occurrences and check if value appears elsewhere
    text_without_boxed = re.sub(r'\\boxed\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', '', assistant_content)
    if boxed in text_without_boxed:
        return assistant_content  # Coherent, boxed value found in solution text

    # Determine the bridging sentence
    if re.match(r'^[A-Da-d]$', boxed.strip()):
        bridge = f"Therefore, the correct option is ({boxed.strip().upper()})."
    else:
        bridge = f"Therefore, the answer is ${boxed}$."

    # Insert before the last \boxed{} line
    idx = assistant_content.rfind('\\boxed{')
    if idx == -1:
        return assistant_content
    # Find the start of the line containing \boxed
    line_start = assistant_content.rfind('\n', 0, idx)
    if line_start == -1:
        line_start = 0
    else:
        line_start += 1
    return assistant_content[:line_start] + bridge + "\n\n" + assistant_content[line_start:]


def fix_missing_answer(assistant_content: str) -> str:
    """For entries with no \\boxed{} and no Answer: marker, try to extract answer."""
    if '\\boxed{' in assistant_content or 'Answer:' in assistant_content:
        return assistant_content

    # Pattern 1: "the answer is X" / "therefore X" / "hence X"
    m = re.search(
        r'(?:the\s+answer\s+is|therefore|hence)\s*[=:]?\s*'
        r'[\$]?([^\$\n,;]{1,80})[\$]?\s*$',
        assistant_content, re.IGNORECASE | re.MULTILINE,
    )
    if m:
        answer = m.group(1).strip().strip('$').strip()
        if answer:
            return assistant_content.rstrip() + f"\n\n$\\boxed{{{answer}}}$"

    # Pattern 2: final displayed equation "= value" at end
    m = re.search(
        r'=\s*[\$]?([^\$\n=]{1,60})[\$]?\s*$',
        assistant_content.rstrip(), re.MULTILINE,
    )
    if m:
        value = m.group(1).strip().strip('$').strip()
        # Only wrap if it looks like a numeric/expression answer
        if value and re.match(r'^[\d\.\-\+\\a-zA-Z{}\s/^_()]+$', value):
            return assistant_content.rstrip() + f"\n\n$\\boxed{{{value}}}$"

    return assistant_content


def fix_long_boxed(assistant_content: str) -> str:
    """Shorten boxed answers that are >200 chars."""
    boxed = _extract_boxed(assistant_content)
    if not boxed or len(boxed) <= 200:
        return assistant_content

    shortened = None

    # If JSON array → extract first element
    if boxed.strip().startswith('['):
        try:
            parsed = json.loads(boxed)
            if isinstance(parsed, list) and parsed:
                shortened = str(parsed[0])
        except (json.JSONDecodeError, ValueError):
            pass

    # If sentence with "is" → extract value after last "is"
    if shortened is None and ' is ' in boxed:
        parts = boxed.rsplit(' is ', 1)
        if len(parts) == 2 and len(parts[1].strip()) < 100:
            shortened = parts[1].strip().rstrip('.')

    # If contains = → extract RHS of last =
    if shortened is None and '=' in boxed:
        parts = boxed.rsplit('=', 1)
        if len(parts) == 2 and len(parts[1].strip()) < 100:
            shortened = parts[1].strip()

    if shortened and len(shortened) <= 200:
        # Replace in the content — find the full boxed expression and swap
        old_boxed = f'\\boxed{{{boxed}}}'
        new_boxed = f'\\boxed{{{shortened}}}'
        return assistant_content.replace(old_boxed, new_boxed, 1)

    return assistant_content


def fix_reverse_letter_mismatch(user_content: str, assistant_content: str) -> str:
    """For non-MCQ questions with bare letter boxed answers where question has
    informal options (A. or A) patterns), add bridging sentence."""
    # Skip if already detected as MCQ (has (A) (B) (C) format)
    mcq_opts = re.findall(r'\(([A-D])\)\s', user_content, re.IGNORECASE)
    if len(set(m.upper() for m in mcq_opts)) >= 3:
        return assistant_content  # Standard MCQ, handled elsewhere

    # Check for informal option patterns: A. or A)
    informal_opts = re.findall(r'(?:^|\n)\s*([A-D])[.)]\s', user_content)
    if len(set(o.upper() for o in informal_opts)) < 3:
        return assistant_content  # No informal options either

    # Check if boxed answer is a bare letter
    boxed = _extract_boxed(assistant_content)
    if not boxed or not re.match(r'^[A-Da-d]$', boxed.strip()):
        return assistant_content

    letter = boxed.strip().upper()

    # Check if bridging sentence already exists
    if re.search(r'correct\s+option\s+is', assistant_content, re.IGNORECASE):
        return assistant_content

    # Insert bridging sentence before boxed
    idx = assistant_content.rfind('\\boxed{')
    if idx == -1:
        return assistant_content
    line_start = assistant_content.rfind('\n', 0, idx)
    if line_start == -1:
        line_start = 0
    else:
        line_start += 1
    bridge = f"The correct option is ({letter})."
    return assistant_content[:line_start] + bridge + "\n\n" + assistant_content[line_start:]


def fix_type_labels(entry: dict) -> dict:
    """Reconcile question_type metadata with actual answer content."""
    meta = entry.get("metadata", {})
    q_type = meta.get("question_type", "")
    assistant = entry["messages"][2]["content"]

    boxed = _extract_boxed(assistant)
    if not boxed:
        return entry

    is_letter = bool(re.match(r'^[A-Da-d]$', boxed.strip()))
    is_numeric = bool(re.match(r'^[\d\.\-\+/\\]+$', boxed.strip()))

    if q_type == "numerical" and is_letter:
        meta["question_type"] = "mcq"
    elif q_type == "mcq" and is_numeric:
        meta["question_type"] = "numerical"

    return entry


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------
def is_jee_relevant(text: str) -> bool:
    """Check if a text sample is relevant to JEE syllabus."""
    text_lower = text.lower()
    return any(kw in text_lower for kw in ALL_JEE_KEYWORDS)


def classify_subject(text: str) -> str:
    """Classify a question into Physics/Chemistry/Mathematics."""
    text_lower = text.lower()
    scores = {
        "Physics": sum(1 for kw in JEE_PHYSICS_KEYWORDS if kw in text_lower),
        "Chemistry": sum(1 for kw in JEE_CHEMISTRY_KEYWORDS if kw in text_lower),
        "Mathematics": sum(1 for kw in JEE_MATH_KEYWORDS if kw in text_lower),
    }
    if max(scores.values()) == 0:
        return "Unknown"
    return max(scores, key=scores.get)


# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------
def load_jsonl(path: Path) -> list[dict]:
    """Load a JSONL file."""
    if not path.exists():
        return []
    records = []
    with open(path) as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


def load_hf_dataset(path: Path) -> list[dict]:
    """Load a HuggingFace arrow dataset from disk."""
    if not path.exists():
        return []
    try:
        from datasets import load_from_disk
        ds = load_from_disk(str(path))
        rows = []
        if hasattr(ds, 'keys'):
            for split in ds:
                rows.extend(ds[split].to_list())
        else:
            rows = ds.to_list()
        return rows
    except Exception as e:
        print(f"  Warning: could not load {path}: {e}")
        return []


def load_parquet_files(directory: Path, patterns: list[str] | None = None) -> list[dict]:
    """Load parquet files from a directory. Optionally filter by filename patterns."""
    import pandas as pd
    if not directory.exists():
        return []
    rows = []
    for pf in sorted(directory.glob("*.parquet")):
        if patterns and not any(p in pf.name for p in patterns):
            continue
        try:
            df = pd.read_parquet(pf)
            rows.extend(df.to_dict("records"))
        except Exception as e:
            print(f"  Warning: could not load {pf}: {e}")
    return rows


def load_json_file(path: Path) -> list[dict]:
    """Load a JSON file (list of dicts)."""
    if not path.exists():
        return []
    try:
        with open(path) as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            # Try common wrapper keys
            for key in ["data", "questions", "examples", "rows"]:
                if key in data and isinstance(data[key], list):
                    return data[key]
            return [data]
        return []
    except Exception as e:
        print(f"  Warning: could not load {path}: {e}")
        return []


def load_tsv_file(path: Path) -> list[dict]:
    """Load a TSV file."""
    import csv
    if not path.exists():
        return []
    rows = []
    try:
        with open(path) as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                rows.append(dict(row))
    except Exception as e:
        print(f"  Warning: could not load {path}: {e}")
    return rows


def load_csv_file(path: Path) -> list[dict]:
    """Load a CSV file."""
    import csv
    if not path.exists():
        return []
    rows = []
    try:
        with open(path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(dict(row))
    except Exception as e:
        print(f"  Warning: could not load {path}: {e}")
    return rows


# ---------------------------------------------------------------------------
# Deduplication against eval sets
# ---------------------------------------------------------------------------
def normalise_text(text: str) -> str:
    """Collapse whitespace, lowercase."""
    return re.sub(r"\s+", " ", text.lower()).strip()


def load_eval_questions() -> list[str]:
    """Load JEEBench eval questions for deduplication."""
    questions = []
    jeebench_path = RAW_DIR / "jeebench" / "jeebench.jsonl"
    if jeebench_path.exists():
        rows = load_jsonl(jeebench_path)
        for r in rows:
            q = r.get("question", r.get("text", ""))
            if q:
                questions.append(normalise_text(q))
    return questions


def is_contaminated(text: str, eval_questions: list[str], threshold: float = 0.85) -> bool:
    """Check if text fuzzy-matches any eval question."""
    norm = normalise_text(text)
    if len(norm) < 50:
        return False
    for eq in eval_questions:
        if len(eq) < 50:
            continue
        # Length pre-filter
        ratio = min(len(norm), len(eq)) / max(len(norm), len(eq))
        if ratio < 0.3:
            continue
        sim = difflib.SequenceMatcher(None, norm, eq).ratio()
        if sim >= threshold:
            return True
    return False


# ---------------------------------------------------------------------------
# Existing formatters
# ---------------------------------------------------------------------------
def format_cot_entry(question: dict) -> dict | None:
    """Convert a CoT-augmented question into mlx-lm chat format."""
    q_text = question.get("question", question.get("problem", question.get("text", "")))
    solution = question.get("cot_solution", "")

    if not q_text or not solution:
        return None

    # Build user message
    user_parts = [q_text.strip()]

    options = question.get("options", question.get("choices", None))
    if options:
        if isinstance(options, list):
            letters = "ABCDEFGH"
            user_parts.append(
                "\n".join(f"({letters[i]}) {opt}" for i, opt in enumerate(options))
            )
        elif isinstance(options, dict):
            user_parts.append("\n".join(f"({k}) {v}" for k, v in options.items()))

    q_type = question.get("type", question.get("question_type", ""))
    if q_type:
        user_parts.append(f"\n[Question type: {q_type}]")

    user_content = "\n\n".join(user_parts)

    # Determine subject (JEEBench uses abbreviations)
    subject = question.get("subject", question.get("topic", ""))
    subject_map = {"phy": "Physics", "chem": "Chemistry", "math": "Mathematics"}
    subject = subject_map.get(subject.lower(), subject) if subject else ""
    if not subject:
        subject = classify_subject(user_content + " " + solution)

    return {
        "messages": [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": solution.strip()},
        ],
        "metadata": {
            "subject": subject,
            "source": question.get("_source", "unknown"),
            "question_type": q_type,
        },
    }


def format_numinamath_entry(question: dict) -> dict | None:
    """Convert a NuminaMath sample into mlx-lm chat format."""
    q_text = question.get("problem", question.get("question", ""))
    solution = question.get("solution", question.get("answer", ""))

    if not q_text or not solution:
        return None

    # NuminaMath is all math, filter for competition-level problems
    source_type = question.get("source", "").lower()
    relevant_sources = ["amc", "aime", "olympiad", "competition", "jee", "iit"]
    if source_type and not any(s in source_type for s in relevant_sources):
        if not is_jee_relevant(q_text):
            return None

    return {
        "messages": [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": q_text.strip()},
            {"role": "assistant", "content": solution.strip()},
        ],
        "metadata": {
            "subject": "Mathematics",
            "source": "numinamath",
            "question_type": "",
        },
    }


# ---------------------------------------------------------------------------
# Math balance formatters (Plan v4)
# ---------------------------------------------------------------------------
# JEE-relevant Competition Math types
_COMP_MATH_JEE_TYPES = {
    "algebra", "intermediate algebra", "precalculus", "geometry",
    "number theory", "counting & probability", "counting and probability",
}


def format_competition_math_entry(row: dict) -> dict | None:
    """Format a Competition Math (MATH dataset) entry into mlx-lm chat format.

    Source: data/raw/math/competition_math/ (HuggingFace arrow, 12,500 entries)
    Schema: problem, solution, level, type
    Filter: Level >= 3, JEE-relevant types
    """
    problem = row.get("problem", "")
    solution = row.get("solution", "")

    if not problem or not solution:
        return None

    # Filter by level (>= 3)
    level_raw = row.get("level", "")
    try:
        # level can be "Level 3" or just "3"
        level_str = str(level_raw).lower().replace("level", "").strip()
        level = int(level_str)
    except (ValueError, TypeError):
        level = 0
    if level < 3:
        return None

    # Filter by JEE-relevant type
    prob_type = (row.get("type", "") or "").lower().strip()
    if prob_type and prob_type not in _COMP_MATH_JEE_TYPES:
        return None

    return {
        "messages": [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": problem.strip()},
            {"role": "assistant", "content": solution.strip()},
        ],
        "metadata": {
            "subject": "Mathematics",
            "source": "competition_math",
            "question_type": "",
        },
    }


# JEE-relevant OpenR1 Math types (matched against problem text or subject field)
_OPENR1_JEE_KEYWORDS = [
    "algebra", "calculus", "geometry", "number theory", "inequalities",
    "trigonometry", "coordinate", "integral", "derivative", "limit",
    "polynomial", "matrix", "determinant", "vector", "probability",
    "combinatorics", "sequence", "series", "conic", "complex number",
]


def format_openr1_math_entry(row: dict) -> dict | None:
    """Format an OpenR1 Math 220k entry into mlx-lm chat format.

    Source: data/raw/math/openr1_math_220k/ (HuggingFace arrow, 93,733 entries)
    Schema: problem, solution, answer, messages, correctness_math_verify, is_reasoning_complete
    Filter: JEE-relevant, must have verified correct solution.
    Strips <think>...</think> tags from model-generated solutions.
    """
    problem = row.get("problem", "")

    if not problem:
        return None

    # Must have verified correct solution
    correctness = row.get("correctness_math_verify")
    if correctness is not None and not correctness:
        return None

    reasoning_complete = row.get("is_reasoning_complete")
    if reasoning_complete is not None and not reasoning_complete:
        return None

    # Get solution: prefer 'solution' field, fall back to messages assistant content
    solution = row.get("solution", "")
    if not solution:
        messages = row.get("messages", [])
        if isinstance(messages, list):
            for msg in messages:
                if isinstance(msg, dict) and msg.get("role") == "assistant":
                    solution = msg.get("content", "")
                    break

    if not solution:
        return None

    # Strip <think>...</think> tags from model-generated solutions
    solution = re.sub(r'<think>.*?</think>', '', solution, flags=re.DOTALL).strip()
    if not solution:
        return None

    # Filter for JEE-relevant content
    combined = (problem + " " + solution).lower()
    if not any(kw in combined for kw in _OPENR1_JEE_KEYWORDS):
        return None

    # Ensure answer is boxed if we have one
    answer = row.get("answer", "")
    if answer and '\\boxed{' not in solution:
        solution = solution.rstrip() + f"\n\n$\\boxed{{{answer}}}$"

    return {
        "messages": [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": problem.strip()},
            {"role": "assistant", "content": solution.strip()},
        ],
        "metadata": {
            "subject": "Mathematics",
            "source": "openr1_math",
            "question_type": "",
        },
    }


# ---------------------------------------------------------------------------
# New source formatters (Change 3)
# ---------------------------------------------------------------------------
def format_physicseval_entry(row: dict) -> dict | None:
    """Format a PhysicsEval entry."""
    # Filter by difficulty
    difficulty = row.get("problem_difficulty", 5)
    try:
        difficulty = int(difficulty)
    except (ValueError, TypeError):
        difficulty = 5
    if not (3 <= difficulty <= 8):
        return None

    # Filter categories
    keep_cats = {
        "mechanics", "thermodynamics", "electromagnetism", "electromagnetic",
        "waves", "optics", "modern physics", "fluid", "solid state",
        "classical mechanics", "quantum", "statistical", "dynamics",
        "circuit", "nuclear", "particle",
    }
    category = (row.get("category", "") or row.get("problem_category", "")).lower()
    if category and not any(k in category for k in keep_cats):
        return None

    # PhysicsEval uses 'problem' field (not 'problem_text')
    q_text = row.get("problem", row.get("problem_text", row.get("question", "")))
    solution = row.get("elaborated_solution_steps", row.get("solution", ""))

    if not q_text or not solution:
        return None

    # Truncate verbose solutions to ~3000 chars, preserving \boxed{} answer
    MAX_SOLUTION_CHARS = 3000
    if len(solution) > MAX_SOLUTION_CHARS:
        # Preserve \boxed{} answer if present
        boxed_match = re.search(r'\$?\\boxed\{[^}]*\}\$?', solution)
        boxed_suffix = ""
        if boxed_match:
            boxed_suffix = "\n\n" + boxed_match.group(0)
        # Truncate to budget, find last paragraph break
        budget = MAX_SOLUTION_CHARS - len(boxed_suffix)
        truncated = solution[:budget]
        last_para = truncated.rfind("\n\n")
        if last_para > budget // 2:
            truncated = truncated[:last_para]
        solution = truncated.rstrip() + boxed_suffix

    # final_answers_in_brief is a list in PhysicsEval
    final_answer_raw = row.get("final_answers_in_brief", row.get("answer", ""))
    if isinstance(final_answer_raw, list):
        # Extract the first answer, try to get the numeric/expression part
        if final_answer_raw:
            final_answer = str(final_answer_raw[0])
        else:
            final_answer = ""
    else:
        final_answer = str(final_answer_raw) if final_answer_raw else ""

    if final_answer and '\\boxed{' not in solution:
        solution = solution.rstrip() + f"\n\n**Answer:** $\\boxed{{{final_answer}}}$"

    return {
        "messages": [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": q_text.strip()},
            {"role": "assistant", "content": solution.strip()},
        ],
        "metadata": {
            "subject": "Physics",
            "source": "physicseval",
            "question_type": "",
        },
    }


def format_physreason_entry(row: dict) -> dict | None:
    """Format a PhysReason entry. Parses JSON structure fields."""
    # Parse question_structure JSON
    q_struct = row.get("question_structure", "")
    if isinstance(q_struct, str):
        try:
            q_struct = json.loads(q_struct)
        except (json.JSONDecodeError, TypeError):
            q_struct = {}

    context = q_struct.get("context", row.get("question", ""))
    sub_questions = q_struct.get("sub_questions", [])

    if not context:
        return None

    # Build question text
    user_parts = [context.strip()]
    if sub_questions and isinstance(sub_questions, list):
        for i, sq in enumerate(sub_questions, 1):
            if isinstance(sq, dict):
                sq_text = sq.get("question", sq.get("text", str(sq)))
            else:
                sq_text = str(sq)
            user_parts.append(f"({i}) {sq_text}")

    user_content = "\n\n".join(user_parts)

    # Parse explanation_steps JSON
    explanation = row.get("explanation_steps", row.get("explanation", ""))
    explanation_parsed = None
    if isinstance(explanation, str):
        try:
            explanation_parsed = json.loads(explanation)
        except (json.JSONDecodeError, TypeError):
            explanation_parsed = None

    if explanation_parsed is not None and isinstance(explanation_parsed, list):
        solution_parts = []
        for i, step in enumerate(explanation_parsed, 1):
            if isinstance(step, dict):
                step_text = step.get("step", step.get("text", str(step)))
            else:
                step_text = str(step)
            solution_parts.append(f"**Step {i}:** {step_text}")
        solution = "\n\n".join(solution_parts)
    elif explanation_parsed is not None and isinstance(explanation_parsed, dict):
        solution_parts = []
        for sq_key in sorted(explanation_parsed.keys()):
            sq_data = explanation_parsed[sq_key]
            sq_label = sq_key.replace("_", " ").title()
            if isinstance(sq_data, dict):
                for step_key in sorted(sq_data.keys()):
                    step_label = step_key.replace("_", " ").title()
                    solution_parts.append(f"**{sq_label}, {step_label}:** {sq_data[step_key]}")
            else:
                solution_parts.append(f"**{sq_label}:** {str(sq_data)}")
        solution = "\n\n".join(solution_parts)
    elif isinstance(explanation, str) and explanation:
        solution = explanation
    else:
        return None

    # Append answers as \boxed{}
    answers = row.get("answer", row.get("answers", []))
    if isinstance(answers, list):
        for ans in answers:
            solution += f"\n\n$\\boxed{{{ans}}}$"
    elif answers:
        solution += f"\n\n$\\boxed{{{answers}}}$"

    if not solution.strip():
        return None

    return {
        "messages": [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": solution.strip()},
        ],
        "metadata": {
            "subject": "Physics",
            "source": "physreason",
            "question_type": "",
        },
    }


def format_scibench_entry(row: dict) -> dict | None:
    """Format a SciBench entry. Maps textbook to subject."""
    # Subject mapping by textbook
    source = (row.get("source", "") or row.get("textbook", "")).lower()

    chem_keywords = ["atkins", "chemmc", "chem"]
    phys_keywords = ["class", "fund", "thermo", "quan", "matter", "halliday", "griffith", "kleppner"]
    skip_keywords = ["stat", "diff", "calculus", "prob"]

    if any(k in source for k in skip_keywords):
        return None

    if any(k in source for k in chem_keywords):
        subject = "Chemistry"
    elif any(k in source for k in phys_keywords):
        subject = "Physics"
    else:
        # Fall back to keyword classification
        q_text = row.get("problem_text", row.get("question", ""))
        subject = classify_subject(q_text or "")
        if subject == "Unknown":
            return None

    q_text = row.get("problem_text", row.get("question", ""))
    solution = row.get("solution", row.get("answer_latex", ""))
    answer = row.get("answer_number", row.get("answer", ""))

    if not q_text:
        return None

    if not solution and answer:
        # Minimal solution with just the answer
        solution = f"**Answer:** $\\boxed{{{answer}}}$"
    elif solution and answer and '\\boxed{' not in solution:
        solution = solution.rstrip() + f"\n\n**Answer:** $\\boxed{{{answer}}}$"

    if not solution:
        return None

    return {
        "messages": [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": q_text.strip()},
            {"role": "assistant", "content": solution.strip()},
        ],
        "metadata": {
            "subject": subject,
            "source": "scibench",
            "question_type": "",
        },
    }


def format_ncert_entry(row: dict, subject: str) -> dict | None:
    """Format an NCERT entry."""
    question = row.get("Question", row.get("question", ""))
    explanation = row.get("Explanation", row.get("explanation", ""))
    answer = row.get("Answer", row.get("answer", ""))

    if not question:
        return None

    # Build solution from explanation + answer
    solution_parts = []
    if explanation and len(str(explanation)) > 100:
        solution_parts.append(str(explanation).strip())
    if answer:
        ans_str = str(answer).strip()
        if '\\boxed{' not in ans_str:
            solution_parts.append(f"**Answer:** $\\boxed{{{ans_str}}}$")
        else:
            solution_parts.append(f"**Answer:** {ans_str}")

    solution = "\n\n".join(solution_parts)

    # Filter: require substantial answer
    if not answer or len(str(answer)) < 10:
        return None

    return {
        "messages": [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": str(question).strip()},
            {"role": "assistant", "content": solution},
        ],
        "metadata": {
            "subject": subject,
            "source": "ncert",
            "question_type": "",
        },
    }


# ---------------------------------------------------------------------------
# Opus queue formatters (for sources needing Opus solution generation)
# ---------------------------------------------------------------------------
def strip_html(text: str) -> str:
    """Strip HTML tags, preserving LaTeX math."""
    # Protect LaTeX
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<p\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</p>', '\n', text, flags=re.IGNORECASE)
    # Remove remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Clean up whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def _parse_entrance_exam_tags(tags_field) -> list[str]:
    """Parse the tags field which is a stringified Python list."""
    if isinstance(tags_field, list):
        return tags_field
    if isinstance(tags_field, str):
        # e.g. "['Chemistry', 'Ionic Equilibrium', 'JEE Advanced']"
        try:
            import ast
            parsed = ast.literal_eval(tags_field)
            if isinstance(parsed, list):
                return [str(t) for t in parsed]
        except (ValueError, SyntaxError):
            return [t.strip().strip("'\"") for t in tags_field.strip("[]").split(",")]
    return []


def _extract_correct_letter(options_html: str) -> str | None:
    """Extract the correct option letter from entrance-exam options HTML."""
    # Look for <li class="correct"> or <li class="... correct ...">
    m = re.search(
        r'<li[^>]*class="[^"]*correct[^"]*"[^>]*>.*?'
        r'<span[^>]*class="option-label"[^>]*>([A-D])</span>',
        options_html, re.DOTALL,
    )
    if m:
        return m.group(1)
    return None


def format_entrance_exam_entry(row: dict) -> dict | None:
    """Format entrance-exam-dataset entry directly to training format.

    The answer field contains full LaTeX solutions wrapped in HTML.
    We strip HTML and use them directly.
    """
    tags = _parse_entrance_exam_tags(row.get("tags", []))
    tags_lower = [t.lower() for t in tags]

    # Filter by Physics or Chemistry
    if "physics" in tags_lower:
        subject = "Physics"
    elif "chemistry" in tags_lower:
        subject = "Chemistry"
    else:
        return None

    question_html = row.get("question", "")
    answer_html = row.get("answer", "")

    if not question_html or not answer_html:
        return None

    # Strip HTML from question and solution
    question = strip_html(question_html)
    solution = strip_html(answer_html)

    if not question or len(question) < 20:
        return None
    if not solution or len(solution) < 50:
        return None

    # Extract and append options if available
    options_html = row.get("options", "")
    correct_letter = None
    if options_html:
        correct_letter = _extract_correct_letter(options_html)
        # Extract option text
        option_matches = re.findall(
            r'<span[^>]*class="option-label"[^>]*>([A-D])</span>\s*'
            r'<span[^>]*class="option-data"[^>]*>(.*?)</span>',
            options_html, re.DOTALL,
        )
        if option_matches:
            opt_lines = []
            for letter, text in option_matches:
                opt_text = strip_html(text).strip()
                if opt_text:
                    opt_lines.append(f"({letter}) {opt_text}")
            if opt_lines:
                question = question + "\n\n" + "\n".join(opt_lines)

    # Add \boxed{} to solution if not present
    if correct_letter and '\\boxed{' not in solution:
        solution = solution.rstrip() + f"\n\n$\\boxed{{{correct_letter}}}$"

    return {
        "messages": [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": question.strip()},
            {"role": "assistant", "content": solution.strip()},
        ],
        "metadata": {
            "subject": subject,
            "source": "entrance_exam",
            "question_type": "mcq" if correct_letter else "",
        },
    }


def format_entrance_exam_for_opus(row: dict, idx: int) -> dict | None:
    """Format entrance-exam-dataset entry for Opus queue (fallback for entries
    without usable solutions)."""
    tags = _parse_entrance_exam_tags(row.get("tags", []))
    tags_lower = [t.lower() for t in tags]

    if "physics" in tags_lower:
        subject = "Physics"
    elif "chemistry" in tags_lower:
        subject = "Chemistry"
    else:
        return None

    question_html = row.get("question", "")
    if not question_html:
        return None

    question = strip_html(question_html)
    if not question or len(question) < 20:
        return None

    # Extract correct answer
    correct_letter = None
    options_html = row.get("options", "")
    if options_html:
        correct_letter = _extract_correct_letter(options_html)

    correct = correct_letter or row.get("correct_option", "")
    correct = strip_html(str(correct))

    gt_type = "mcq" if correct_letter else "subjective"

    return {
        "id": f"entrance_exam_{subject.lower()[:4]}_{idx:04d}",
        "question": question,
        "ground_truth": str(correct),
        "ground_truth_type": gt_type,
        "source": "entrance_exam",
        "subject": subject,
        "existing_solution": None,
        "reason": "new_source",
    }


def format_chemistryqa_for_opus(row: dict, idx: int) -> dict | None:
    """Format ChemistryQA entry for Opus queue."""
    # Filter by JEE-relevant topic
    jee_topics = {
        "physical chemistry", "organic", "inorganic", "electrochemistry",
        "kinetics", "thermodynamics", "equilibrium", "atomic structure",
        "bonding", "coordination", "chemical bonding", "solutions",
        "solid state", "surface chemistry",
    }
    topic = (row.get("topic", "") or row.get("category", "")).lower()
    if topic and not any(t in topic for t in jee_topics):
        # Fall back to keyword matching
        q = row.get("question", "")
        if not is_jee_relevant(q):
            return None

    question = row.get("question", "")
    correct = row.get("correct_answer", row.get("answer", ""))

    if not question or not correct:
        return None

    gt_type = "mcq" if re.search(r'\([A-D]\)', question) else "subjective"
    if re.match(r'^[\d.\-]+$', str(correct).strip()):
        gt_type = "numerical"

    return {
        "id": f"chemistryqa_{idx:04d}",
        "question": question.strip(),
        "ground_truth": str(correct),
        "ground_truth_type": gt_type,
        "source": "chemistryqa",
        "subject": "Chemistry",
        "existing_solution": None,
        "reason": "new_source",
    }


def format_gpqa_for_opus(row: dict, idx: int) -> dict | None:
    """Format GPQA Diamond entry for Opus queue."""
    # Filter by physics or chemistry subdomain
    subdomain = (row.get("Subdomain", "") or row.get("subdomain", "") or row.get("domain", "")).lower()
    high_domain = (row.get("High-level domain", "") or "").lower()
    phys_terms = {"physics", "mechanics", "quantum", "electro", "thermo", "optics", "astrophysics", "photonics", "condensed matter", "particle"}
    chem_terms = {"chemistry", "organic", "inorganic", "biochem"}

    if high_domain == "physics" or any(t in subdomain for t in phys_terms):
        subject = "Physics"
    elif high_domain == "chemistry" or any(t in subdomain for t in chem_terms):
        subject = "Chemistry"
    else:
        return None

    question_text = row.get("Question", row.get("question", ""))
    correct = row.get("Correct Answer", row.get("correct_answer", ""))
    incorrect_1 = row.get("Incorrect Answer 1", row.get("incorrect_answer_1", ""))
    incorrect_2 = row.get("Incorrect Answer 2", row.get("incorrect_answer_2", ""))
    incorrect_3 = row.get("Incorrect Answer 3", row.get("incorrect_answer_3", ""))

    if not question_text or not correct:
        return None

    # Shuffle options
    options = [correct, incorrect_1, incorrect_2, incorrect_3]
    options = [o for o in options if o]  # filter empty
    random.shuffle(options)

    correct_letter = None
    letters = "ABCD"
    option_lines = []
    for i, opt in enumerate(options[:4]):
        option_lines.append(f"({letters[i]}) {opt}")
        if opt == correct:
            correct_letter = letters[i]

    if not correct_letter:
        return None

    full_question = question_text.strip() + "\n\n" + "\n".join(option_lines)

    return {
        "id": f"gpqa_{subject.lower()[:4]}_{idx:04d}",
        "question": full_question,
        "ground_truth": correct_letter,
        "ground_truth_type": "mcq",
        "source": "gpqa",
        "subject": subject,
        "existing_solution": None,
        "reason": "new_source",
    }


# ---------------------------------------------------------------------------
# Merge Opus solutions
# ---------------------------------------------------------------------------
def merge_opus_solutions():
    """Merge reconciled Opus solutions into train/valid files."""
    opus_path = DATA_DIR / "opus_solutions.jsonl"
    if not opus_path.exists():
        print(f"Error: {opus_path} not found. Run generate_opus_solutions.py first.")
        sys.exit(1)

    # Load existing data
    train_full_path = DATA_DIR / "train_full.jsonl"
    valid_full_path = DATA_DIR / "valid_full.jsonl"
    train_data = load_jsonl(train_full_path)
    valid_data = load_jsonl(valid_full_path)

    print(f"Existing: {len(train_data)} train + {len(valid_data)} valid")

    # Load Opus solutions (only reconciled=true)
    opus_entries = []
    with open(opus_path) as f:
        for line in f:
            if line.strip():
                entry = json.loads(line)
                if entry.get("reconciled"):
                    opus_entries.append(entry)

    print(f"Opus solutions: {len(opus_entries)} reconciled entries")

    # Format into training examples
    new_examples = []
    for entry in opus_entries:
        solution = entry.get("solution", "")
        question = entry.get("question", "")
        subject = entry.get("subject", "Unknown")
        source = entry.get("source", "opus")

        if not question or not solution:
            continue

        ex = {
            "messages": [
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": question.strip()},
                {"role": "assistant", "content": solution.strip()},
            ],
            "metadata": {
                "subject": subject,
                "source": source,
                "question_type": entry.get("ground_truth_type", ""),
            },
        }

        # Apply LaTeX cleaning
        cleaned = clean_latex(ex["messages"][2]["content"])
        if cleaned is None:
            continue
        ex["messages"][2]["content"] = cleaned

        # Apply MCQ fix
        ex["messages"][2]["content"] = fix_mcq_answer(
            ex["messages"][1]["content"], ex["messages"][2]["content"]
        )

        # Validate
        if not is_valid_entry(ex):
            continue

        new_examples.append(ex)

    print(f"Valid Opus examples: {len(new_examples)}")

    # Merge: add to combined pool, re-shuffle, re-split
    all_examples = train_data + valid_data + new_examples
    random.seed(42)
    random.shuffle(all_examples)

    split_idx = int(len(all_examples) * TRAIN_SPLIT)
    train_data = all_examples[:split_idx]
    valid_data = all_examples[split_idx:]

    # Write files
    _write_output_files(train_data, valid_data)

    # Log distribution
    _log_distribution(all_examples)

    print(f"\nMerged {len(new_examples)} Opus solutions into dataset.")


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------
def _write_output_files(train_data: list[dict], valid_data: list[dict]):
    """Write train/valid JSONL files (both stripped and full)."""
    train_path = DATA_DIR / "train.jsonl"
    valid_path = DATA_DIR / "valid.jsonl"
    full_train_path = DATA_DIR / "train_full.jsonl"
    full_valid_path = DATA_DIR / "valid_full.jsonl"

    with open(train_path, "w") as f:
        for ex in train_data:
            f.write(json.dumps({"messages": ex["messages"]}, ensure_ascii=False) + "\n")

    with open(valid_path, "w") as f:
        for ex in valid_data:
            f.write(json.dumps({"messages": ex["messages"]}, ensure_ascii=False) + "\n")

    with open(full_train_path, "w") as f:
        for ex in train_data:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    with open(full_valid_path, "w") as f:
        for ex in valid_data:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    print(f"\nSaved:")
    print(f"  Training:   {train_path} ({len(train_data)} examples)")
    print(f"  Validation: {valid_path} ({len(valid_data)} examples)")
    print(f"  Full train: {full_train_path}")
    print(f"  Full valid: {full_valid_path}")


def _log_distribution(all_examples: list[dict]):
    """Log subject and source distribution."""
    subjects = collections.Counter()
    sources = collections.Counter()
    for ex in all_examples:
        meta = ex.get("metadata", {})
        subjects[meta.get("subject", "Unknown")] += 1
        sources[meta.get("source", "unknown")] += 1

    total = len(all_examples)
    print(f"\nSubject distribution (n={total}):")
    for subj, count in subjects.most_common():
        print(f"  {subj}: {count} ({count/total:.1%})")

    print(f"\nSource distribution:")
    for src, count in sources.most_common():
        print(f"  {src}: {count} ({count/total:.1%})")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Format data for MLX-LM SFT training")
    parser.add_argument("--merge-opus", action="store_true",
                        help="Merge Opus solutions into train/valid")
    args = parser.parse_args()

    if args.merge_opus:
        print("=" * 60)
        print("Merging Opus solutions into training data")
        print("=" * 60)
        merge_opus_solutions()
        return

    print("=" * 60)
    print("Phase 1c: Formatting data for MLX-LM SFT training")
    print("=" * 60)

    # Load eval questions for dedup
    print("\nLoading eval questions for deduplication...")
    eval_questions = load_eval_questions()
    print(f"  {len(eval_questions)} eval questions loaded")

    all_examples = []
    opus_queue = []

    # ---------------------------------------------------------------
    # 1. Process CoT-augmented datasets (highest priority)
    # ---------------------------------------------------------------
    print("\n[1] Processing CoT-augmented datasets...")
    for cot_file in sorted(COT_DIR.glob("*_cot.jsonl")):
        source_name = cot_file.stem.replace("_cot", "")
        records = load_jsonl(cot_file)
        formatted = 0
        for r in tqdm(records, desc=f"  {source_name}"):
            r["_source"] = source_name
            entry = format_cot_entry(r)
            if entry:
                all_examples.append(entry)
                formatted += 1
        print(f"  {source_name}: {formatted}/{len(records)} formatted")

    # ---------------------------------------------------------------
    # 2. Process NuminaMath (cap 3000)
    # ---------------------------------------------------------------
    print("\n[2] Processing NuminaMath (filtering for competition math)...")
    numinamath_records = load_jsonl(RAW_DIR / "numinamath" / "numinamath.jsonl")
    numa_formatted = 0
    MAX_NUMINAMATH = 3000
    random.shuffle(numinamath_records)
    for r in tqdm(numinamath_records, desc="  numinamath"):
        if numa_formatted >= MAX_NUMINAMATH:
            break
        entry = format_numinamath_entry(r)
        if entry:
            all_examples.append(entry)
            numa_formatted += 1
    print(f"  numinamath: {numa_formatted} selected (capped at {MAX_NUMINAMATH})")

    # ---------------------------------------------------------------
    # 2b. Process Competition Math (cap 1200)
    # ---------------------------------------------------------------
    print("\n[2b] Processing Competition Math (MATH dataset)...")
    comp_math_path = RAW_DIR / "math" / "competition_math"
    comp_math_rows = load_hf_dataset(comp_math_path)
    if not comp_math_rows:
        comp_math_rows = load_jsonl(comp_math_path / "competition_math.jsonl")
    if not comp_math_rows:
        comp_math_rows = load_json_file(comp_math_path / "train.json")
    cm_formatted = 0
    MAX_COMPETITION_MATH = 1200
    random.shuffle(comp_math_rows)
    for r in tqdm(comp_math_rows, desc="  competition_math"):
        if cm_formatted >= MAX_COMPETITION_MATH:
            break
        entry = format_competition_math_entry(r)
        if entry:
            if is_contaminated(entry["messages"][1]["content"], eval_questions):
                continue
            all_examples.append(entry)
            cm_formatted += 1
    print(f"  competition_math: {cm_formatted} selected (capped at {MAX_COMPETITION_MATH})")

    # ---------------------------------------------------------------
    # 2c. Process OpenR1 Math 220k (cap 800)
    # ---------------------------------------------------------------
    print("\n[2c] Processing OpenR1 Math 220k...")
    openr1_path = RAW_DIR / "math" / "openr1_math_220k"
    openr1_rows = load_hf_dataset(openr1_path)
    if not openr1_rows:
        openr1_rows = load_jsonl(openr1_path / "openr1_math.jsonl")
    or1_formatted = 0
    MAX_OPENR1_MATH = 800
    random.shuffle(openr1_rows)
    for r in tqdm(openr1_rows, desc="  openr1_math"):
        if or1_formatted >= MAX_OPENR1_MATH:
            break
        entry = format_openr1_math_entry(r)
        if entry:
            if is_contaminated(entry["messages"][1]["content"], eval_questions):
                continue
            all_examples.append(entry)
            or1_formatted += 1
    print(f"  openr1_math: {or1_formatted} selected (capped at {MAX_OPENR1_MATH})")

    # ---------------------------------------------------------------
    # 3. Process PhysicsEval (cap 1200) — JSON format
    # ---------------------------------------------------------------
    print("\n[3] Processing PhysicsEval (cap 1200)...")
    physicseval_path = RAW_DIR / "physics" / "physicseval"
    # PhysicsEval ships as train.json / test.json
    physicseval_rows = load_json_file(physicseval_path / "train.json")
    if not physicseval_rows:
        physicseval_rows = load_hf_dataset(physicseval_path)
    if not physicseval_rows:
        physicseval_rows = load_jsonl(physicseval_path / "physicseval.jsonl")
    pe_formatted = 0
    MAX_PHYSICSEVAL = 1200
    random.shuffle(physicseval_rows)
    pe_skipped_contam = 0
    for r in tqdm(physicseval_rows, desc="  physicseval"):
        if pe_formatted >= MAX_PHYSICSEVAL:
            break
        entry = format_physicseval_entry(r)
        if entry:
            # Dedup against eval
            if is_contaminated(entry["messages"][1]["content"], eval_questions):
                pe_skipped_contam += 1
                continue
            all_examples.append(entry)
            pe_formatted += 1
    print(f"  physicseval: {pe_formatted} selected (capped at {MAX_PHYSICSEVAL}, {pe_skipped_contam} eval-contaminated)")

    # ---------------------------------------------------------------
    # 4. Process PhysReason (no cap)
    # ---------------------------------------------------------------
    print("\n[4] Processing PhysReason...")
    physreason_path = RAW_DIR / "physics" / "physreason"
    physreason_rows = load_hf_dataset(physreason_path)
    if not physreason_rows:
        physreason_rows = load_jsonl(physreason_path / "physreason.jsonl")
    pr_formatted = 0
    pr_skipped_contam = 0
    for r in tqdm(physreason_rows, desc="  physreason"):
        entry = format_physreason_entry(r)
        if entry:
            if is_contaminated(entry["messages"][1]["content"], eval_questions):
                pr_skipped_contam += 1
                continue
            all_examples.append(entry)
            pr_formatted += 1
    print(f"  physreason: {pr_formatted} formatted ({pr_skipped_contam} eval-contaminated)")

    # ---------------------------------------------------------------
    # 5. Process SciBench (no cap)
    # ---------------------------------------------------------------
    print("\n[5] Processing SciBench...")
    scibench_path = RAW_DIR / "science" / "scibench"
    scibench_rows = load_hf_dataset(scibench_path)
    if not scibench_rows:
        scibench_rows = load_jsonl(scibench_path / "scibench.jsonl")
    sb_formatted = 0
    sb_skipped_contam = 0
    for r in tqdm(scibench_rows, desc="  scibench"):
        entry = format_scibench_entry(r)
        if entry:
            if is_contaminated(entry["messages"][1]["content"], eval_questions):
                sb_skipped_contam += 1
                continue
            all_examples.append(entry)
            sb_formatted += 1
    print(f"  scibench: {sb_formatted} formatted ({sb_skipped_contam} eval-contaminated)")

    # ---------------------------------------------------------------
    # 6. Process NCERT Physics + Chemistry (cap 400/subject)
    # ---------------------------------------------------------------
    print("\n[6] Processing NCERT...")
    ncert_path = RAW_DIR / "ncert"
    ncert_subjects = {
        "Physics": ["physics_11th", "physics_12th"],
        "Chemistry": ["chemistry_11th", "chemistry_12th"],
    }
    MAX_NCERT_PER_SUBJECT = 400

    for subject, subdirs in ncert_subjects.items():
        ncert_formatted = 0
        all_ncert_rows = []
        for subdir in subdirs:
            path = ncert_path / subdir
            rows = load_hf_dataset(path)
            if not rows:
                for jsonl_file in sorted(path.glob("*.jsonl")) if path.exists() else []:
                    rows.extend(load_jsonl(jsonl_file))
            all_ncert_rows.extend(rows)
        random.shuffle(all_ncert_rows)
        for r in tqdm(all_ncert_rows, desc=f"  ncert/{subject}"):
            if ncert_formatted >= MAX_NCERT_PER_SUBJECT:
                break
            entry = format_ncert_entry(r, subject)
            if entry:
                if is_contaminated(entry["messages"][1]["content"], eval_questions):
                    continue
                all_examples.append(entry)
                ncert_formatted += 1
        print(f"  ncert/{subject}: {ncert_formatted} (capped at {MAX_NCERT_PER_SUBJECT})")

    # ---------------------------------------------------------------
    # 7. Process entrance-exam-dataset (direct to training — has solutions)
    #    Parquet format: ADVANCED + MAIN files for JEE-relevant content
    # ---------------------------------------------------------------
    print("\n[7] Processing entrance-exam-dataset...")
    entrance_path = RAW_DIR / "entrance_exam"
    # Load only JEE-relevant exams (ADVANCED + MAIN), skip NEET/NDA/WBJEE/BITSAT
    entrance_rows = load_parquet_files(entrance_path, patterns=["ADVANCED", "MAIN"])
    if not entrance_rows:
        entrance_rows = load_hf_dataset(entrance_path)
    MAX_ENTRANCE_EXAM = 5000
    MAX_ENTRANCE_EXAM_PHYSICS = 1800
    random.shuffle(entrance_rows)
    ee_formatted = 0
    ee_physics_count = 0
    ee_opus_queued = 0
    ee_skipped_contam = 0
    ee_skipped_physics_cap = 0
    for idx, r in enumerate(tqdm(entrance_rows, desc="  entrance_exam")):
        if ee_formatted >= MAX_ENTRANCE_EXAM:
            break
        # Try direct format first (has full HTML solutions)
        entry = format_entrance_exam_entry(r)
        if entry:
            if is_contaminated(entry["messages"][1]["content"], eval_questions):
                ee_skipped_contam += 1
                continue
            # Enforce per-subject physics cap
            if entry["metadata"]["subject"] == "Physics" and ee_physics_count >= MAX_ENTRANCE_EXAM_PHYSICS:
                ee_skipped_physics_cap += 1
                continue
            all_examples.append(entry)
            ee_formatted += 1
            if entry["metadata"]["subject"] == "Physics":
                ee_physics_count += 1
        else:
            # Fallback to opus queue for entries without usable solutions
            opus_entry = format_entrance_exam_for_opus(r, idx)
            if opus_entry:
                if not is_contaminated(opus_entry["question"], eval_questions):
                    opus_queue.append(opus_entry)
                    ee_opus_queued += 1
    print(f"  entrance_exam: {ee_formatted} direct + {ee_opus_queued} opus-queued ({ee_skipped_contam} eval-contaminated, {ee_skipped_physics_cap} physics-capped)")

    # ---------------------------------------------------------------
    # 8b. Process ChemistryQA (opus queue — TSV format)
    # ---------------------------------------------------------------
    print("\n[8b] Building Opus queue (ChemistryQA, GPQA)...")

    # ChemistryQA — TSV format
    chemqa_path = RAW_DIR / "chemistry" / "chemistryqa"
    chemqa_rows = load_tsv_file(chemqa_path / "train.tsv")
    if not chemqa_rows:
        chemqa_rows = load_hf_dataset(chemqa_path)
    cq_queued = 0
    for idx, r in enumerate(tqdm(chemqa_rows, desc="  chemistryqa")):
        entry = format_chemistryqa_for_opus(r, idx)
        if entry:
            if is_contaminated(entry["question"], eval_questions):
                continue
            opus_queue.append(entry)
            cq_queued += 1
    print(f"  chemistryqa: {cq_queued} queued for Opus")

    # GPQA Diamond (gated — may not be available)
    gpqa_path = RAW_DIR / "science" / "gpqa"
    gpqa_rows = load_csv_file(gpqa_path / "gpqa_diamond.csv")
    if not gpqa_rows:
        gpqa_rows = load_hf_dataset(gpqa_path)
    if not gpqa_rows:
        gpqa_rows = load_jsonl(gpqa_path / "gpqa.jsonl")
    gp_queued = 0
    if gpqa_rows:
        for idx, r in enumerate(tqdm(gpqa_rows, desc="  gpqa")):
            entry = format_gpqa_for_opus(r, idx)
            if entry:
                if is_contaminated(entry["question"], eval_questions):
                    continue
                opus_queue.append(entry)
                gp_queued += 1
        print(f"  gpqa: {gp_queued} queued for Opus")
    else:
        print(f"  gpqa: skipped (dataset not available — gated)")

    # ---------------------------------------------------------------
    # 9. Apply LaTeX cleaning to all assistant messages
    # ---------------------------------------------------------------
    print(f"\n[9] Applying LaTeX cleaning...")
    cleaned_examples = []
    latex_dropped = 0
    for ex in all_examples:
        cleaned = clean_latex(ex["messages"][2]["content"])
        if cleaned is None:
            latex_dropped += 1
            continue
        ex["messages"][2]["content"] = cleaned
        cleaned_examples.append(ex)
    print(f"  Dropped {latex_dropped} entries (CJK/mojibake)")
    all_examples = cleaned_examples

    # ---------------------------------------------------------------
    # 10. Apply MCQ answer fix
    # ---------------------------------------------------------------
    print(f"\n[10] Applying MCQ answer fix...")
    mcq_fixed = 0
    for ex in all_examples:
        user = ex["messages"][1]["content"]
        asst = ex["messages"][2]["content"]
        fixed = fix_mcq_answer(user, asst)
        if fixed != asst:
            ex["messages"][2]["content"] = fixed
            mcq_fixed += 1
    print(f"  Fixed {mcq_fixed} MCQ answers")

    # ---------------------------------------------------------------
    # 10a. Fix coherence (boxed answer not found in solution text)
    # ---------------------------------------------------------------
    print(f"\n[10a] Fixing coherence issues...")
    coherence_fixed = 0
    for ex in all_examples:
        asst = ex["messages"][2]["content"]
        fixed = fix_coherence_answer(asst)
        if fixed != asst:
            ex["messages"][2]["content"] = fixed
            coherence_fixed += 1
    print(f"  Fixed {coherence_fixed} coherence issues")

    # ---------------------------------------------------------------
    # 10b. Fix missing answers
    # ---------------------------------------------------------------
    print(f"\n[10b] Fixing missing answers...")
    missing_fixed = 0
    for ex in all_examples:
        asst = ex["messages"][2]["content"]
        fixed = fix_missing_answer(asst)
        if fixed != asst:
            ex["messages"][2]["content"] = fixed
            missing_fixed += 1
    print(f"  Fixed {missing_fixed} missing answers")

    # ---------------------------------------------------------------
    # 10c. Fix long boxed answers (>200 chars)
    # ---------------------------------------------------------------
    print(f"\n[10c] Fixing long boxed answers...")
    long_boxed_fixed = 0
    for ex in all_examples:
        asst = ex["messages"][2]["content"]
        fixed = fix_long_boxed(asst)
        if fixed != asst:
            ex["messages"][2]["content"] = fixed
            long_boxed_fixed += 1
    print(f"  Fixed {long_boxed_fixed} long boxed answers")

    # ---------------------------------------------------------------
    # 10d. Fix reverse letter mismatches
    # ---------------------------------------------------------------
    print(f"\n[10d] Fixing reverse letter mismatches...")
    reverse_fixed = 0
    for ex in all_examples:
        user = ex["messages"][1]["content"]
        asst = ex["messages"][2]["content"]
        fixed = fix_reverse_letter_mismatch(user, asst)
        if fixed != asst:
            ex["messages"][2]["content"] = fixed
            reverse_fixed += 1
    print(f"  Fixed {reverse_fixed} reverse letter mismatches")

    # ---------------------------------------------------------------
    # 10e. Fix type label mismatches
    # ---------------------------------------------------------------
    print(f"\n[10e] Fixing type label mismatches...")
    type_fixed = 0
    for ex in all_examples:
        old_type = ex.get("metadata", {}).get("question_type", "")
        ex = fix_type_labels(ex)
        if ex.get("metadata", {}).get("question_type", "") != old_type:
            type_fixed += 1
    print(f"  Fixed {type_fixed} type label mismatches")

    # ---------------------------------------------------------------
    # 11. Apply is_valid_entry filter
    # ---------------------------------------------------------------
    print(f"\n[11] Validating LaTeX structure...")
    valid_examples = []
    latex_invalid = 0
    for ex in all_examples:
        if is_valid_entry(ex):
            valid_examples.append(ex)
        else:
            latex_invalid += 1
    print(f"  Dropped {latex_invalid} entries (invalid LaTeX)")
    all_examples = valid_examples

    # ---------------------------------------------------------------
    # 12. Shuffle, split, save
    # ---------------------------------------------------------------
    print(f"\n[12] Total examples: {len(all_examples)}")
    random.seed(42)
    random.shuffle(all_examples)

    split_idx = int(len(all_examples) * TRAIN_SPLIT)
    train_data = all_examples[:split_idx]
    valid_data = all_examples[split_idx:]

    _write_output_files(train_data, valid_data)

    # ---------------------------------------------------------------
    # 13. Write Opus queue
    # ---------------------------------------------------------------
    if opus_queue:
        opus_queue_path = DATA_DIR / "opus_queue.jsonl"
        with open(opus_queue_path, "w") as f:
            for entry in opus_queue:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print(f"\n  Opus queue: {opus_queue_path} ({len(opus_queue)} entries)")

        # Opus queue subject distribution
        opus_subjects = collections.Counter(e["subject"] for e in opus_queue)
        opus_sources = collections.Counter(e["source"] for e in opus_queue)
        print(f"  Opus queue by subject: {dict(opus_subjects)}")
        print(f"  Opus queue by source: {dict(opus_sources)}")

    # ---------------------------------------------------------------
    # 14. Log distribution stats
    # ---------------------------------------------------------------
    _log_distribution(all_examples)


if __name__ == "__main__":
    main()
