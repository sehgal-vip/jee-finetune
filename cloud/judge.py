"""
Phase 3d: LLM-as-Judge verifier for SDPO training.

This module provides the reward/feedback function integrated into SDPO rollouts:
  1. Extracts the model's final answer from its response
  2. Rule-based check: correct or wrong
  3. If wrong: calls Claude Opus 4.6 for rich step-level feedback
  4. If correct: returns brief confirmation
  5. Caches judge responses to avoid redundant API calls
"""

import hashlib
import json
import os
import re
from pathlib import Path

import anthropic

# Judge configuration defaults
DEFAULT_MODEL = "claude-opus-4-6-20250929"
DEFAULT_MAX_TOKENS = 2048
NUMERICAL_TOLERANCE = 0.01  # 1%

# Cache for judge responses
_judge_cache: dict[str, str] = {}
_cache_file: Path | None = None


def init_cache(cache_path: str = "judge_cache.jsonl"):
    """Load existing judge response cache."""
    global _judge_cache, _cache_file
    _cache_file = Path(cache_path)
    if _cache_file.exists():
        with open(_cache_file) as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    _judge_cache[entry["key"]] = entry["feedback"]
        print(f"Loaded {len(_judge_cache)} cached judge responses")


def _cache_key(question: str, model_output: str, ground_truth: str) -> str:
    """Generate cache key from question + output + ground truth."""
    combined = f"{question}|||{model_output}|||{ground_truth}"
    return hashlib.sha256(combined.encode()).hexdigest()[:20]


def _save_cache_entry(key: str, feedback: str):
    """Append a feedback entry to the cache file."""
    if _cache_file:
        with open(_cache_file, "a") as f:
            f.write(json.dumps({"key": key, "feedback": feedback}) + "\n")


def extract_answer(response: str) -> str:
    """Extract the final answer from a model's response.

    Handles:
      - **Answer:** (X) patterns
      - MCQ letter answers: (A), (B), (C), (D)
      - Numerical answers
      - The answer is X patterns
    """
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

    # Pattern 4: Last line with option letter
    lines = response.strip().split("\n")
    for line in reversed(lines):
        match = re.search(r"\(([A-D])\)", line)
        if match:
            return match.group(1)

    return ""


def normalize_answer(answer: str) -> str:
    """Normalize an answer for comparison."""
    answer = answer.strip().lower()
    # Remove wrapping parentheses and dollar signs
    answer = re.sub(r"^\((.+)\)$", r"\1", answer)
    answer = re.sub(r"^\$(.+)\$$", r"\1", answer)
    # Remove LaTeX formatting
    answer = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", answer)
    answer = re.sub(r"[\\{}\s]", "", answer)
    return answer


def check_answer(generated: str, ground_truth: str) -> tuple[bool, str]:
    """Check if the generated answer matches ground truth.

    Returns (is_correct, detail_message).
    """
    gen = normalize_answer(generated)
    gt = normalize_answer(str(ground_truth))

    if not gen:
        return False, f"Could not extract answer from response"

    if not gt:
        return False, "No ground truth available"

    # Exact match
    if gen == gt:
        return True, "Exact match"

    # Containment check
    if gt in gen or gen in gt:
        return True, "Partial match"

    # Numerical comparison with tolerance
    try:
        gen_num = float(re.sub(r"[^0-9.\-e]", "", gen))
        gt_num = float(re.sub(r"[^0-9.\-e]", "", gt))
        if gt_num != 0:
            rel_error = abs(gen_num - gt_num) / abs(gt_num)
            if rel_error < NUMERICAL_TOLERANCE:
                return True, f"Numerical match (error: {rel_error:.4f})"
            else:
                return False, f"Numerical mismatch: got {gen_num}, expected {gt_num} (error: {rel_error:.4f})"
        elif abs(gen_num - gt_num) < 1e-6:
            return True, "Numerical match (near zero)"
        else:
            return False, f"Numerical mismatch: got {gen_num}, expected {gt_num}"
    except (ValueError, ZeroDivisionError):
        pass

    # Multi-answer MCQ (e.g., "A,C" vs "AC")
    gen_letters = set(re.findall(r"[a-d]", gen))
    gt_letters = set(re.findall(r"[a-d]", gt))
    if gen_letters and gt_letters:
        if gen_letters == gt_letters:
            return True, "MCQ match"
        else:
            return False, f"MCQ mismatch: got {gen_letters}, expected {gt_letters}"

    return False, f"No match: '{generated}' vs '{ground_truth}'"


def get_judge_feedback(
    question: str,
    model_output: str,
    ground_truth: str,
    client: anthropic.Anthropic | None = None,
    config: dict | None = None,
) -> dict:
    """Get rich feedback from the LLM judge.

    Returns a dict with:
      - is_correct: bool
      - answer_extracted: str
      - feedback: str (rich textual feedback for SDPO)
      - detail: str (match detail)
      - from_cache: bool
    """
    if config is None:
        config = {}

    model = config.get("model", DEFAULT_MODEL)
    max_tokens = config.get("max_tokens", DEFAULT_MAX_TOKENS)

    # Step 1: Extract the model's answer
    answer_extracted = extract_answer(model_output)

    # Step 2: Rule-based check
    is_correct, detail = check_answer(answer_extracted, ground_truth)

    # Step 3: Check cache
    cache_key = _cache_key(question, model_output, ground_truth)
    if cache_key in _judge_cache:
        return {
            "is_correct": is_correct,
            "answer_extracted": answer_extracted,
            "feedback": _judge_cache[cache_key],
            "detail": detail,
            "from_cache": True,
        }

    # Step 4: Generate feedback via LLM judge
    if client is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            return {
                "is_correct": is_correct,
                "answer_extracted": answer_extracted,
                "feedback": f"[No API key] {'Correct' if is_correct else 'Incorrect'}: {detail}",
                "detail": detail,
                "from_cache": False,
            }
        client = anthropic.Anthropic(api_key=api_key)

    system_prompt = config.get(
        "system_prompt",
        "You are an expert IIT JEE examiner evaluating a student's solution. "
        "Analyze the solution step-by-step. If correct, confirm briefly. "
        "If wrong, identify exactly where the reasoning went wrong, "
        "which concept was misapplied, and what the correct approach should be.",
    )

    if is_correct:
        user_prompt = (
            f"Question: {question}\n"
            f"Correct answer: {ground_truth}\n"
            f"Student's solution: {model_output}\n\n"
            f"The student's answer is correct. Provide brief confirmation of the "
            f"correct approach and key concepts used (2-3 sentences)."
        )
    else:
        user_prompt = (
            f"Question: {question}\n"
            f"Correct answer: {ground_truth}\n"
            f"Student's solution: {model_output}\n\n"
            f"Analyze the student's solution step-by-step. Identify exactly where "
            f"the reasoning went wrong, which concept was misapplied, and what "
            f"the correct approach should be. Be specific and educational."
        )

    try:
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        feedback = response.content[0].text
    except Exception as e:
        feedback = f"[Judge API error: {e}] {'Correct' if is_correct else 'Incorrect'}: {detail}"

    # Cache the feedback
    _judge_cache[cache_key] = feedback
    _save_cache_entry(cache_key, feedback)

    return {
        "is_correct": is_correct,
        "answer_extracted": answer_extracted,
        "feedback": feedback,
        "detail": detail,
        "from_cache": False,
    }


def batch_judge(
    rollouts: list[dict],
    client: anthropic.Anthropic | None = None,
    config: dict | None = None,
) -> list[dict]:
    """Judge a batch of rollouts.

    Each rollout should have: question, model_output, ground_truth.
    Returns a list of feedback dicts.
    """
    results = []
    for rollout in rollouts:
        result = get_judge_feedback(
            question=rollout["question"],
            model_output=rollout["model_output"],
            ground_truth=rollout["ground_truth"],
            client=client,
            config=config,
        )
        results.append(result)
    return results


if __name__ == "__main__":
    # Quick test
    init_cache("test_judge_cache.jsonl")

    test_question = "A particle of mass 2 kg is projected vertically upward with velocity 20 m/s. Find max height. (g=10 m/s²)"
    test_output = "Using v² = u² - 2gh\n0 = 400 - 20h\nh = 20m\n\n**Answer:** 20 m"
    test_gt = "20"

    result = get_judge_feedback(test_question, test_output, test_gt)
    print(json.dumps(result, indent=2))
