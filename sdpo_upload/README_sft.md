---
library_name: mlx
license: apache-2.0
license_link: https://huggingface.co/Qwen/Qwen3-8B/blob/main/LICENSE
pipeline_tag: text-generation
base_model: Qwen/Qwen3-8B-MLX-4bit
tags:
- qwen3
- jee
- iit-jee
- math
- physics
- chemistry
- sft
- lora
- chain-of-thought
- mlx
datasets:
- daman1209arora/jeebench
- AI-MO/NuminaMath-CoT
language:
- en
model-index:
- name: qwen3-8b-jee-sft
  results:
  - task:
      type: question-answering
      name: JEE Advanced Problem Solving
    dataset:
      type: daman1209arora/jeebench
      name: JEEBench (200-question eval split)
    metrics:
    - type: accuracy
      value: 45.0
      name: Overall Accuracy
    - type: accuracy
      value: 54.5
      name: Mathematics Accuracy
    - type: accuracy
      value: 50.0
      name: Chemistry Accuracy
    - type: accuracy
      value: 29.7
      name: Physics Accuracy
---

# Qwen3-8B JEE SFT

A fine-tuned version of [Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) specialized for solving **IIT JEE Advanced** problems in Physics, Chemistry, and Mathematics with detailed chain-of-thought reasoning.

This model was trained via **supervised fine-tuning (SFT)** using QLoRA on Apple Silicon with [MLX](https://github.com/ml-explore/mlx-lm).

## Model Details

| Property | Value |
|---|---|
| **Base Model** | [Qwen/Qwen3-8B-MLX-4bit](https://huggingface.co/Qwen/Qwen3-8B-MLX-4bit) |
| **Method** | QLoRA (4-bit) supervised fine-tuning |
| **Format** | Full-precision safetensors (bfloat16) |
| **Size** | ~16.4 GB |
| **Architecture** | Qwen3ForCausalLM, 36 layers, 32 heads, 4096 hidden |

## Training Details

- **Framework**: [MLX](https://github.com/ml-explore/mlx-lm) on Apple M3 Pro
- **Method**: QLoRA — LoRA adapters on a 4-bit quantized base model
- **Data**: 3,515 examples (3,163 train / 352 validation)
  - **JEEBench CoT**: 457 JEE Advanced questions with Claude Opus 4.6-generated step-by-step solutions (Physics, Chemistry, Mathematics)
  - **NuminaMath-CoT**: 2,706 filtered competition math problems (AMC, AIME, Olympiad-level)

### Hyperparameters

| Parameter | Value |
|---|---|
| Learning rate | 1e-5 |
| Iterations | 3,500 |
| Batch size | 1 |
| Gradient accumulation steps | 4 |
| LoRA rank | 8 |
| LoRA scale (alpha/rank) | 20.0 |
| LoRA dropout | 0.0 |
| LoRA layers | 8 (top layers) |
| Max sequence length | 2,048 |
| Optimizer | Adam |
| Gradient checkpointing | Enabled |

## Evaluation Results

Evaluated on 200 held-out questions from [JEEBench](https://huggingface.co/datasets/daman1209arora/jeebench) covering Physics, Chemistry, and Mathematics. All models used greedy decoding with max 2,048 tokens.

| Subject | Base Qwen3-8B | SFT (this model) | Delta |
|---|---|---|---|
| **Overall** | 78/200 (39.0%) | **90/200 (45.0%)** | **+6.0%** |
| Mathematics | 24/66 (36.4%) | **36/66 (54.5%)** | **+18.2%** |
| Chemistry | 32/70 (45.7%) | **35/70 (50.0%)** | **+4.3%** |
| Physics | **22/64 (34.4%)** | 19/64 (29.7%) | -4.7% |

**Key takeaways:**
- SFT improves overall accuracy by **+6 percentage points** over the base model
- Largest gain is in **Mathematics (+18.2%)**, driven by competition math training data (NuminaMath-CoT)
- Chemistry shows a modest improvement (+4.3%)
- Physics slightly regressed (-4.7%), likely due to the training data being skewed toward mathematics (~83% of examples)


## Usage

### With MLX on Apple Silicon

```bash
pip install mlx-lm

mlx_lm.generate \
    --model vipsehgal/qwen3-8b-jee-sft \
    --prompt "Solve: Find the number of real solutions of x^3 - 3x + 1 = 0"
```

### With Transformers

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("vipsehgal/qwen3-8b-jee-sft", torch_dtype="auto", device_map="auto")
tokenizer = AutoTokenizer.from_pretrained("vipsehgal/qwen3-8b-jee-sft")

messages = [
    {"role": "system", "content": "You are an expert IIT JEE tutor. Solve problems step-by-step using LaTeX notation. Show all work clearly and arrive at the final answer."},
    {"role": "user", "content": "A particle of mass 2 kg is projected vertically upward with velocity 20 m/s. Find the maximum height reached. (Take g = 10 m/s^2)"}
]

text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(text, return_tensors="pt").to(model.device)
output = model.generate(**inputs, max_new_tokens=1024)
print(tokenizer.decode(output[0], skip_special_tokens=True))
```

## System Prompt

```
You are an expert IIT JEE tutor. Solve problems step-by-step using LaTeX notation. Show all work clearly and arrive at the final answer.
```

## Related Models

| Model | Size | Description |
|---|---|---|
| **vipsehgal/qwen3-8b-jee-sft** | **16.4 GB** | **SFT model (bf16) — this model** |

## Limitations

- Training data is skewed toward mathematics (~83%) vs physics/chemistry (~17%), which limits gains on science subjects
- Physics performance slightly regressed compared to the base model
- May produce incorrect reasoning steps while arriving at correct final answers — always verify solutions
- Evaluated on 200 questions; full 515-question JEEBench benchmark not yet run

## License

Apache 2.0 (following the [base Qwen3-8B license](https://huggingface.co/Qwen/Qwen3-8B/blob/main/LICENSE))
