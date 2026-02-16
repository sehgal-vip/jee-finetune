#!/usr/bin/env python3
"""
Generate Chain-of-Thought solutions for CAMEL-AI Physics & Chemistry datasets
using Claude API.

Usage:
    export ANTHROPIC_API_KEY='sk-ant-...'
    python scripts/generate_camel_cot.py [--subject physics|chemistry|both] [--max N] [--batch-size N]
"""

import argparse
import asyncio
import json
import os
import time
from pathlib import Path

import anthropic
from datasets import load_from_disk

# Configuration
MODEL = "claude-sonnet-4-5-20250929"  # Sonnet for cost efficiency on 40K questions
MAX_TOKENS = 2048
CONCURRENT_REQUESTS = 10
OUTPUT_DIR = Path("data/cot")

SYSTEM_PROMPT = (
    "You are an expert IIT JEE tutor. Solve problems step-by-step using LaTeX notation. "
    "Show all work clearly and arrive at the final answer. "
    "Use $...$ for inline math and $$...$$ for display math. "
    "End with \\boxed{answer}."
)


def load_camel_dataset(subject: str) -> list[dict]:
    """Load CAMEL-AI physics or chemistry dataset."""
    path = f"data/raw/{subject}/camel_{subject}"

    if not Path(path).exists():
        print(f"Dataset not found at {path}, trying HuggingFace download...")
        from datasets import load_dataset
        ds = load_dataset(f"camel-ai/{subject}")
        ds.save_to_disk(path)

    ds = load_from_disk(path)

    # Handle DatasetDict vs Dataset
    if hasattr(ds, 'keys'):
        # It's a DatasetDict, get the first split
        split_name = list(ds.keys())[0]
        ds = ds[split_name]

    questions = []
    for i, row in enumerate(ds):
        # CAMEL-AI format: message_1 (user question), message_2 (assistant answer)
        question = row.get("message_1", row.get("instruction", row.get("question", "")))
        existing_answer = row.get("message_2", row.get("output", row.get("answer", "")))

        if question:
            questions.append({
                "id": f"camel_{subject}_{i}",
                "question": question,
                "existing_answer": existing_answer,
                "subject": subject.capitalize(),
                "source": f"camel-ai/{subject}",
            })

    return questions


async def generate_cot_solution(
    client: anthropic.AsyncAnthropic,
    question: dict,
    semaphore: asyncio.Semaphore,
    retry_count: int = 3,
) -> dict:
    """Generate a CoT solution for a single question."""
    async with semaphore:
        for attempt in range(retry_count):
            try:
                response = await client.messages.create(
                    model=MODEL,
                    max_tokens=MAX_TOKENS,
                    system=SYSTEM_PROMPT,
                    messages=[{
                        "role": "user",
                        "content": question["question"],
                    }],
                )

                solution = response.content[0].text
                return {
                    **question,
                    "cot_solution": solution,
                    "model_used": MODEL,
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                }
            except anthropic.RateLimitError:
                wait = 2 ** attempt * 5
                print(f"  Rate limited, waiting {wait}s...")
                await asyncio.sleep(wait)
            except Exception as e:
                if attempt == retry_count - 1:
                    print(f"  Failed after {retry_count} attempts: {e}")
                    return {**question, "cot_solution": "", "error": str(e)}
                await asyncio.sleep(2)

    return {**question, "cot_solution": "", "error": "max retries exceeded"}


async def process_batch(
    client: anthropic.AsyncAnthropic,
    questions: list[dict],
    output_path: Path,
    batch_size: int = 50,
):
    """Process questions in batches with progress tracking."""
    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)

    total = len(questions)
    completed = 0
    total_input_tokens = 0
    total_output_tokens = 0
    start_time = time.time()

    # Check for existing progress
    existing_ids = set()
    if output_path.exists():
        with open(output_path) as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    existing_ids.add(entry["id"])
        print(f"Found {len(existing_ids)} existing solutions, resuming...")

    # Filter out already processed
    remaining = [q for q in questions if q["id"] not in existing_ids]
    completed = len(existing_ids)
    print(f"Processing {len(remaining)} remaining questions (of {total} total)")

    # Process in batches
    for i in range(0, len(remaining), batch_size):
        batch = remaining[i:i + batch_size]

        tasks = [
            generate_cot_solution(client, q, semaphore)
            for q in batch
        ]
        results = await asyncio.gather(*tasks)

        # Save results
        with open(output_path, "a") as f:
            for result in results:
                if result.get("cot_solution"):
                    f.write(json.dumps(result) + "\n")
                    total_input_tokens += result.get("input_tokens", 0)
                    total_output_tokens += result.get("output_tokens", 0)
                    completed += 1

        elapsed = time.time() - start_time
        rate = completed / elapsed * 60 if elapsed > 0 else 0
        est_cost = (total_input_tokens * 3 / 1_000_000) + (total_output_tokens * 15 / 1_000_000)

        print(
            f"  Progress: {completed}/{total} ({completed/total*100:.1f}%) | "
            f"Rate: {rate:.0f}/min | "
            f"Tokens: {total_input_tokens + total_output_tokens:,} | "
            f"Est cost: ${est_cost:.2f}"
        )


def main():
    parser = argparse.ArgumentParser(description="Generate CoT solutions for CAMEL-AI datasets")
    parser.add_argument("--subject", choices=["physics", "chemistry", "both"], default="both")
    parser.add_argument("--max", type=int, default=0, help="Max questions per subject (0=all)")
    parser.add_argument("--batch-size", type=int, default=50)
    parser.add_argument("--concurrent", type=int, default=10)
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: Set ANTHROPIC_API_KEY environment variable")
        print("  export ANTHROPIC_API_KEY='sk-ant-...'")
        exit(1)

    global CONCURRENT_REQUESTS
    CONCURRENT_REQUESTS = args.concurrent

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    client = anthropic.AsyncAnthropic(api_key=api_key)

    subjects = ["physics", "chemistry"] if args.subject == "both" else [args.subject]

    for subject in subjects:
        print(f"\n{'='*60}")
        print(f"Generating CoT solutions for CAMEL-AI {subject.upper()}")
        print(f"{'='*60}")

        questions = load_camel_dataset(subject)
        print(f"Loaded {len(questions)} questions")

        if args.max > 0:
            questions = questions[:args.max]
            print(f"Limited to {len(questions)} questions")

        output_path = OUTPUT_DIR / f"camel_{subject}_cot.jsonl"

        asyncio.run(process_batch(client, questions, output_path, args.batch_size))

        # Count results
        count = 0
        if output_path.exists():
            with open(output_path) as f:
                count = sum(1 for line in f if line.strip())
        print(f"\nSaved {count} solutions to {output_path}")

    print("\n" + "="*60)
    print("CoT generation complete!")
    print("="*60)


if __name__ == "__main__":
    main()
