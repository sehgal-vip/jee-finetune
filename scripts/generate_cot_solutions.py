#!/usr/bin/env python3
"""
Phase 1b: Generate chain-of-thought solutions using Claude Opus 4.6.

Reads raw JEE questions, generates step-by-step LaTeX solutions via the
Anthropic API, verifies the final answer matches ground truth, and saves
the augmented dataset.

Requires: ANTHROPIC_API_KEY environment variable.
"""

import asyncio
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

import anthropic
from tqdm import tqdm

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
COT_DIR = DATA_DIR / "cot"
CACHE_DIR = DATA_DIR / "cache"

MODEL = "claude-opus-4-6-20250929"
MAX_TOKENS = 4096
MAX_CONCURRENT = 5  # parallel API calls
RETRY_ATTEMPTS = 3
RETRY_DELAY = 5  # seconds


SYSTEM_PROMPT = """You are an expert IIT JEE tutor with deep knowledge of Physics, Chemistry, and Mathematics at the JEE Advanced level.

When given a problem and its correct answer, produce a detailed step-by-step solution that:
1. Identifies the key concepts and principles involved
2. Shows all intermediate steps with clear reasoning
3. Uses proper LaTeX notation for all mathematical expressions ($...$ inline, $$...$$ display)
4. Arrives at the correct answer naturally through the solution steps
5. Ends with a clearly marked final answer

Format your solution as:
**Step 1:** [First step with explanation]

**Step 2:** [Next step]
...

**Answer:** [Final answer matching the correct answer]"""


def build_question_prompt(question: dict) -> str:
    """Build the user prompt from a question dict."""
    parts = []

    # Extract question text
    q_text = question.get("question", question.get("problem", question.get("text", "")))
    if not q_text:
        return ""

    parts.append(f"**Question:**\n{q_text}")

    # Add options if MCQ
    options = question.get("options", question.get("choices", None))
    if options:
        if isinstance(options, list):
            option_letters = "ABCDEFGH"
            opts_text = "\n".join(
                f"({option_letters[i]}) {opt}" for i, opt in enumerate(options)
            )
        elif isinstance(options, dict):
            opts_text = "\n".join(f"({k}) {v}" for k, v in options.items())
        else:
            opts_text = str(options)
        parts.append(f"\n**Options:**\n{opts_text}")

    # Add correct answer (JEEBench uses "gold")
    answer = question.get("answer", question.get("gold", question.get("correct_answer", question.get("solution", ""))))
    if answer:
        parts.append(f"\n**Correct Answer:** {answer}")

    # Add question type hint
    q_type = question.get("type", question.get("question_type", ""))
    if q_type:
        parts.append(f"\n**Question Type:** {q_type}")

    # Add subject
    subject = question.get("subject", question.get("topic", ""))
    if subject:
        parts.append(f"\n**Subject:** {subject}")

    parts.append("\nPlease provide a detailed step-by-step solution arriving at the correct answer.")

    return "\n".join(parts)


def get_cache_key(question_prompt: str) -> str:
    """Generate a cache key for a question."""
    return hashlib.sha256(question_prompt.encode()).hexdigest()[:16]


def load_cache() -> dict:
    """Load cached CoT solutions."""
    cache = {}
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / "cot_cache.jsonl"
    if cache_file.exists():
        with open(cache_file) as f:
            for line in f:
                entry = json.loads(line)
                cache[entry["key"]] = entry["solution"]
    return cache


def save_to_cache(key: str, solution: str):
    """Append a solution to the cache."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / "cot_cache.jsonl"
    with open(cache_file, "a") as f:
        f.write(json.dumps({"key": key, "solution": solution}) + "\n")


def extract_final_answer(solution: str) -> str:
    """Extract the final answer from a generated solution."""
    # Look for **Answer:** pattern
    match = re.search(r"\*\*Answer:\*\*\s*(.+?)(?:\n|$)", solution)
    if match:
        return match.group(1).strip()
    # Fallback: look for "Answer:" without bold
    match = re.search(r"Answer:\s*(.+?)(?:\n|$)", solution)
    if match:
        return match.group(1).strip()
    return ""


def normalize_answer(answer: str) -> str:
    """Normalize an answer for comparison."""
    answer = answer.strip().lower()
    # Remove common wrappers
    answer = re.sub(r"^\((.+)\)$", r"\1", answer)
    answer = re.sub(r"^\$(.+)\$$", r"\1", answer)
    answer = re.sub(r"[\\{}\s]", "", answer)
    return answer


def answers_match(generated: str, ground_truth: str) -> bool:
    """Check if a generated answer matches ground truth."""
    gen = normalize_answer(generated)
    gt = normalize_answer(str(ground_truth))

    if not gen or not gt:
        return False

    # Exact match
    if gen == gt:
        return True

    # Check if ground truth is contained in generated (e.g., "(B)" in "The answer is (B)")
    if gt in gen or gen in gt:
        return True

    # Numerical comparison with tolerance
    try:
        gen_num = float(re.sub(r"[^0-9.\-e]", "", gen))
        gt_num = float(re.sub(r"[^0-9.\-e]", "", gt))
        if gt_num != 0:
            return abs(gen_num - gt_num) / abs(gt_num) < 0.01  # 1% tolerance
        return abs(gen_num - gt_num) < 1e-6
    except (ValueError, ZeroDivisionError):
        pass

    return False


async def generate_solution(
    client: anthropic.AsyncAnthropic,
    question: dict,
    semaphore: asyncio.Semaphore,
    cache: dict,
) -> dict | None:
    """Generate a CoT solution for a single question."""
    prompt = build_question_prompt(question)
    if not prompt:
        return None

    cache_key = get_cache_key(prompt)
    if cache_key in cache:
        return {**question, "cot_solution": cache[cache_key], "from_cache": True}

    async with semaphore:
        for attempt in range(RETRY_ATTEMPTS):
            try:
                response = await client.messages.create(
                    model=MODEL,
                    max_tokens=MAX_TOKENS,
                    system=SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": prompt}],
                )
                solution = response.content[0].text

                # Verify the answer matches
                generated_answer = extract_final_answer(solution)
                ground_truth = question.get(
                    "answer",
                    question.get("gold", question.get("correct_answer", question.get("solution", ""))),
                )

                if ground_truth and not answers_match(generated_answer, str(ground_truth)):
                    # Retry with a more explicit prompt
                    if attempt < RETRY_ATTEMPTS - 1:
                        continue
                    else:
                        # Log mismatch but still save (human review later)
                        solution += f"\n\n[WARNING: Generated answer '{generated_answer}' may not match ground truth '{ground_truth}']"

                save_to_cache(cache_key, solution)
                return {**question, "cot_solution": solution, "from_cache": False}

            except anthropic.RateLimitError:
                wait = RETRY_DELAY * (2**attempt)
                print(f"  Rate limited, waiting {wait}s...")
                await asyncio.sleep(wait)
            except anthropic.APIError as e:
                if attempt < RETRY_ATTEMPTS - 1:
                    await asyncio.sleep(RETRY_DELAY)
                else:
                    print(f"  API error after {RETRY_ATTEMPTS} attempts: {e}")
                    return None

    return None


async def process_dataset(
    dataset_name: str, questions: list[dict], client: anthropic.AsyncAnthropic
) -> list[dict]:
    """Process an entire dataset of questions."""
    print(f"\nProcessing {dataset_name}: {len(questions)} questions")

    cache = load_cache()
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    tasks = [
        generate_solution(client, q, semaphore, cache)
        for q in questions
    ]

    results = []
    for coro in tqdm(
        asyncio.as_completed(tasks),
        total=len(tasks),
        desc=f"  {dataset_name}",
    ):
        result = await coro
        if result is not None:
            results.append(result)

    return results


def load_raw_questions(dataset_name: str) -> list[dict]:
    """Load raw questions from a downloaded dataset."""
    jsonl_path = RAW_DIR / dataset_name / f"{dataset_name}.jsonl"
    if not jsonl_path.exists():
        print(f"  Warning: {jsonl_path} not found, skipping.")
        return []

    questions = []
    with open(jsonl_path) as f:
        for line in f:
            if line.strip():
                questions.append(json.loads(line))
    return questions


async def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        print("Export it: export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)

    print("=" * 60)
    print("Phase 1b: Generating chain-of-thought solutions via Claude Opus")
    print("=" * 60)

    COT_DIR.mkdir(parents=True, exist_ok=True)
    client = anthropic.AsyncAnthropic(api_key=api_key)

    # Priority: JEEBench first (core dataset), then Kaggle JEE, then filter
    # relevant samples from SciInstruct and NuminaMath
    datasets_to_process = ["jeebench", "kaggle_jee"]

    total_generated = 0
    total_cached = 0

    for ds_name in datasets_to_process:
        questions = load_raw_questions(ds_name)
        if not questions:
            continue

        results = await process_dataset(ds_name, questions, client)

        # Save results
        out_path = COT_DIR / f"{ds_name}_cot.jsonl"
        with open(out_path, "w") as f:
            for r in results:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

        cached = sum(1 for r in results if r.get("from_cache", False))
        generated = len(results) - cached
        total_generated += generated
        total_cached += cached

        print(f"  {ds_name}: {len(results)} solutions ({generated} new, {cached} cached)")
        print(f"  Saved to {out_path}")

    # For SciInstruct and NuminaMath, these already have solutions
    # We just need to filter for JEE-relevant content
    print("\nNote: SciInstruct and NuminaMath already contain solutions.")
    print("They will be filtered for JEE-relevant content in the formatting step.")

    print(f"\nTotal: {total_generated} new solutions generated, {total_cached} from cache")


if __name__ == "__main__":
    asyncio.run(main())
