# JEE-Level Training Datasets: Comprehensive Research Report

## Date: 2026-02-15

---

## 1. DIRECTLY JEE/NEET-TARGETED DATASETS

### 1.1 JEEBench (DAIR-IITD)
- **URL**: https://github.com/dair-iitd/jeebench
- **HuggingFace**: https://huggingface.co/datasets/daman1209arora/jeebench
- **Size**: 515 problems
- **Subjects**: Physics, Chemistry, Mathematics
- **Source**: JEE Advanced 2016-2023 (8 editions)
- **Solutions**: Yes (step-by-step solutions, GPT model responses included)
- **Format**: JSON (zipped), with few-shot examples
- **Question Types**: MCQ (single/multi-correct), integer-type, matching
- **Paper**: "Have LLMs Advanced Enough?" (EMNLP 2023)
- **JEE Relevance**: **HIGHEST** - Directly from JEE Advanced papers. Gold standard for JEE evaluation.

### 1.2 JEE-NEET Benchmark (Reja1)
- **URL**: https://huggingface.co/datasets/Reja1/jee-neet-benchmark
- **Size**: Covers JEE Main, JEE Advanced, and NEET questions (image-based)
- **Subjects**: Physics, Chemistry, Mathematics (JEE); Physics, Chemistry, Biology (NEET)
- **Solutions**: Yes (correct answers with metadata)
- **Format**: Image-based questions with JSON metadata (question_id, subject, correct_answer)
- **Answer Types**: MCQ option identifiers, INTEGER numerical answers
- **JEE Relevance**: **HIGHEST** - Directly from JEE/NEET exams. Multimodal (image input required).

### 1.3 JEE AND NEET Question JSON Format (Kaggle)
- **URL**: https://www.kaggle.com/datasets/damerajee/jee-question-json-format
- **Size**: Not precisely documented (estimated hundreds to thousands of questions)
- **Subjects**: Physics, Chemistry, Mathematics
- **Solutions**: Yes (answers included)
- **Format**: JSON
- **JEE Relevance**: **HIGHEST** - Direct JEE/NEET questions in structured format.

### 1.4 IITJEE NEET AIIMS Students Questions Data (Kaggle)
- **URL**: https://www.kaggle.com/datasets/mrutyunjaybiswal/iitjee-neet-aims-students-questions-data
- **Size**: Not precisely documented
- **Subjects**: Physics, Chemistry, Mathematics, Biology
- **Solutions**: Questions with subject classification
- **Format**: CSV/tabular
- **Related**: Questions Chapter Classification dataset by same author
- **JEE Relevance**: **HIGH** - Student-level questions from JEE/NEET/AIIMS preparation.

### 1.5 MedMCQA
- **URL**: https://github.com/medmcqa/medmcqa | https://huggingface.co/datasets/openlifescienceai/medmcqa
- **Size**: 194,000+ MCQs
- **Subjects**: 21 medical subjects, 2,400 healthcare topics
- **Source**: AIIMS PG & NEET PG entrance exams (1991-present)
- **Solutions**: Yes (detailed explanations for each question)
- **Format**: JSON with question, options, correct answer, explanation
- **Split**: Train (mock/online tests), Test (AIIMS PG), Dev (NEET PG)
- **License**: Available for research
- **JEE Relevance**: **MEDIUM** - Medical entrance (not engineering), but covers Biology/Chemistry at competitive level. Useful for NEET Biology/Chemistry training.

---

## 2. NCERT & INDIAN CURRICULUM DATASETS

### 2.1 NCERT Dataset Collection (KadamParth - HuggingFace)
- **URL**: https://huggingface.co/collections/KadamParth/ncert-dataset
- **Individual datasets**:
  - Physics 11th: https://huggingface.co/datasets/KadamParth/NCERT_Physics_11th
  - Physics 12th: https://huggingface.co/datasets/KadamParth/NCERT_Physics_12th
  - Chemistry 11th: https://huggingface.co/datasets/KadamParth/NCERT_Chemistry_11th
  - Chemistry 12th: https://huggingface.co/datasets/KadamParth/NCERT_Chemistry_12th
  - Biology 11th: https://huggingface.co/datasets/KadamParth/NCERT_Biology_11th
  - Biology 12th: https://huggingface.co/datasets/KadamParth/NCERT_Biology_12th
- **Size**: Textbook content for standards 6-12
- **Subjects**: Physics, Chemistry, Biology, History, Political Science
- **Solutions**: Textbook content (not Q&A format)
- **Format**: HuggingFace datasets format
- **JEE Relevance**: **HIGH** - NCERT is the foundational curriculum for JEE/NEET. Essential for building domain knowledge.

### 2.2 NCERT Dataset (Kaggle - pateldhruvikiranbhai)
- **URL**: https://www.kaggle.com/datasets/pateldhruvikiranbhai/ncert-dataset
- **Size**: Not precisely documented
- **Subjects**: Multiple subjects from NCERT curriculum
- **Format**: Kaggle dataset format
- **JEE Relevance**: **HIGH** - NCERT foundational content.

### 2.3 NCERT-MD (Kaggle)
- **URL**: https://www.kaggle.com/datasets/jbalwaysus/ncert-md
- **Size**: Not precisely documented
- **Subjects**: NCERT content in Markdown format
- **Format**: Markdown files
- **JEE Relevance**: **HIGH** - Clean text format of NCERT content, good for LLM training.

### 2.4 EXAMS-QA (Multi-Subject High School Examinations)
- **URL**: https://github.com/mhardalov/exams-qa | https://huggingface.co/datasets/exams
- **Size**: 24,000+ questions in 26 languages
- **Subjects**: Biology, Chemistry, Geography, History, Physics, Agriculture, Geology, Informatics
- **Solutions**: Yes (correct answer labels)
- **Format**: JSONL
- **Paper**: EMNLP 2020
- **JEE Relevance**: **MEDIUM** - High school matriculation exams from multiple countries. Some physics/chemistry content at comparable level.

---

## 3. SCIENCE QUESTION-ANSWERING DATASETS

### 3.1 SciQ (Allen AI)
- **URL**: https://allenai.org/data/sciq/ | https://www.kaggle.com/datasets/thedevastator/sciq-a-dataset-for-science-question-answering | https://huggingface.co/datasets/allenai/sciq
- **Size**: 13,679 questions
- **Subjects**: Physics, Chemistry, Biology, Earth Science
- **Solutions**: Yes (correct answer + supporting paragraph)
- **Format**: JSON with question, correct_answer, distractor1-3, support
- **License**: CC BY-NC 3.0
- **JEE Relevance**: **MEDIUM** - General science MCQs. Difficulty level is below JEE but useful for foundational training.

### 3.2 ScienceQA
- **URL**: https://scienceqa.github.io/ | https://huggingface.co/datasets/derek-thomas/ScienceQA
- **Size**: ~21,000 multimodal MCQs (94.3k rows total with splits)
- **Subjects**: Natural Science, Language Science, Social Science (26 topics, 127 categories, 379 skills)
- **Solutions**: Yes (lectures + explanations + step-by-step solutions)
- **Format**: Parquet with image, question, choices, answer, hint, lecture, solution fields
- **Split**: Train 75.4k, Val 9.43k, Test 9.43k
- **JEE Relevance**: **MEDIUM** - Multimodal science questions with explanations. Grade school to high school level. Good for building reasoning chains.

### 3.3 ARC - AI2 Reasoning Challenge
- **URL**: https://huggingface.co/datasets/allenai/ai2_arc | https://www.kaggle.com/datasets/jeromeblanchet/arc-ai2-reasoning-challenge
- **Size**: 7,787 questions (Challenge: 2,590 + Easy: 5,197)
- **Subjects**: Grade-school science (physics, chemistry, biology, earth science)
- **Solutions**: Yes (correct answer labels)
- **Format**: JSON with question, choices, answerKey
- **Corpus**: 14 million+ science sentences included
- **JEE Relevance**: **LOW-MEDIUM** - Grade school level, but the Challenge set requires multi-step reasoning useful for building reasoning capabilities.

### 3.4 OpenBookQA
- **URL**: https://www.kaggle.com/datasets/thedevastator/openbookqa-a-new-dataset-for-advanced-question-a
- **Size**: ~6,000 questions
- **Subjects**: Elementary science
- **Solutions**: Yes
- **Format**: JSON
- **JEE Relevance**: **LOW** - Elementary level, but tests multi-step reasoning with open-book science facts.

---

## 4. MATHEMATICS DATASETS

### 4.1 MATH Dataset (Hendrycks)
- **URL**: https://github.com/hendrycks/math | https://huggingface.co/datasets/hendrycks/competition_math
- **Size**: 12,500 problems
- **Subjects**: Algebra, Counting & Probability, Geometry, Intermediate Algebra, Number Theory, Prealgebra, Precalculus
- **Source**: AMC 10, AMC 12, AIME competitions
- **Solutions**: Yes (full step-by-step solutions in LaTeX)
- **Format**: JSON with problem text and solution in LaTeX + natural language
- **Difficulty**: 5 levels (1-5)
- **JEE Relevance**: **HIGH** - Competition math at similar difficulty to JEE Mathematics. Step-by-step solutions are excellent for chain-of-thought training.

### 4.2 AMPS (Auxiliary Mathematics Problems and Solutions)
- **URL**: https://github.com/hendrycks/math (download link in repo)
- **Size**: 23GB, 5 million+ problems
- **Subjects**: Elementary math through multivariable calculus (including Stokes' theorem)
- **Source**: Khan Academy (100k+ problems, 693 exercise types) + Mathematica-generated problems
- **Solutions**: Yes (step-by-step solutions in LaTeX)
- **Format**: LaTeX text files
- **JEE Relevance**: **HIGH** - Massive pretraining dataset covering fundamentals through calculus. Excellent for building mathematical reasoning foundations.

### 4.3 NuminaMath
- **URL**: https://huggingface.co/datasets/AI-MO/NuminaMath-CoT | https://huggingface.co/collections/AI-MO/numinamath
- **Size**: 860,000 problem-solution pairs
- **Subjects**: Math at all levels (high school to olympiad)
- **Source**: Chinese high school math, US/international olympiad problems
- **Solutions**: Yes (Chain-of-Thought formatted solutions)
- **Format**: HuggingFace dataset with CoT traces
- **Extended**: NuminaMath-QwQ-CoT-5M has 5 million reasoning traces
- **JEE Relevance**: **HIGH** - Broad math coverage including competition-level problems. CoT format ideal for training reasoning.

### 4.4 Math Olympiad Problems and Solutions (AoPS - Kaggle)
- **URL**: https://www.kaggle.com/datasets/imbishal7/math-olympiad-problems-and-solutions-aops
- **Size**: Not precisely documented (AoPS-Instruct related dataset has 650k+ Q&A pairs)
- **Subjects**: Olympiad-level mathematics (Algebra, Combinatorics, Geometry, Number Theory)
- **Solutions**: Yes
- **Format**: Kaggle dataset
- **JEE Relevance**: **HIGH** - Olympiad math problems are at or above JEE Advanced level.

### 4.5 AIMO-OlympiadBench-Math-Dataset (Kaggle)
- **URL**: https://www.kaggle.com/datasets/kishanvavdara/aimo-olympiadbench-math-dataset
- **Size**: Subset of OlympiadBench (math portion)
- **Subjects**: Competition Mathematics
- **Solutions**: Yes
- **Format**: Kaggle dataset
- **JEE Relevance**: **HIGH** - Olympiad-level math competition problems.

### 4.6 MathQA
- **URL**: https://www.kaggle.com/datasets/thedevastator/dataset-for-solving-math-word-problems
- **Size**: ~37,000 problems
- **Subjects**: General mathematics word problems
- **Solutions**: Yes
- **Format**: JSON
- **JEE Relevance**: **MEDIUM** - Math word problems, useful for problem comprehension training.

### 4.7 Mathematical Problems Dataset
- **URL**: https://www.kaggle.com/datasets/thedevastator/mathematical-problems-dataset-various-mathematic
- **Size**: Various
- **Subjects**: Multiple math topics
- **Format**: Kaggle dataset
- **JEE Relevance**: **MEDIUM**

---

## 5. ADVANCED SCIENTIFIC REASONING BENCHMARKS

### 5.1 TheoremQA
- **URL**: https://github.com/TIGER-AI-Lab/TheoremQA | https://huggingface.co/datasets/TIGER-Lab/TheoremQA
- **Size**: 800 questions covering 350 theorems
- **Subjects**: Math (199 theorems, 442 questions), Physics (52 theorems, 131 questions), CS&EE (48 theorems, 146 questions), Finance (55 theorems, 81 questions)
- **Solutions**: Yes (with theorem references)
- **Format**: JSON with some image inputs (51 questions with diagrams)
- **Paper**: EMNLP 2023
- **Difficulty**: University-level theorem application
- **JEE Relevance**: **HIGH** - Theorem-driven problem solving at university level. Physics and Math content directly applicable. Tests deep conceptual understanding.

### 5.2 SciBench
- **URL**: https://github.com/mandyyyyii/scibench | https://scibench-ucla.github.io/
- **Size**: 789 problems + 94 multimodal problems
- **Subjects**: College-level Chemistry, Physics, Mathematics
- **Source**: Widely-used college textbooks
- **Solutions**: Yes (open-ended free-response with multi-step solutions)
- **Format**: JSON with LaTeX; multimodal subset includes graphs/figures
- **Paper**: ICML 2024
- **Difficulty**: College-level (requires calculus, differential equations, domain knowledge)
- **JEE Relevance**: **HIGH** - College-level scientific problem solving. Difficulty comparable to or above JEE Advanced. Tests multi-step reasoning, concept retrieval, and complex computation.

### 5.3 OlympiadBench
- **URL**: https://github.com/OpenBMB/OlympiadBench | https://huggingface.co/datasets/Hothan/OlympiadBench
- **Size**: 8,476 problems
- **Subjects**: Mathematics + Physics (from international olympiads, Chinese olympiads, GaoKao)
- **Solutions**: Yes (expert-level step-by-step annotations)
- **Format**: JSON with images, bilingual (English + Chinese)
- **Question Types**: Open-ended, MCQ, Fill-in-blank, Judgement
- **Answer Types**: Numeric, Expression, Equation, Interval, Tuple
- **Paper**: ACL 2024
- **JEE Relevance**: **VERY HIGH** - Olympiad-level physics and math. Includes Chinese college entrance exam (GaoKao) which is comparable to JEE. Bilingual, multimodal, expert-annotated.

### 5.4 MMLU (Massive Multitask Language Understanding)
- **URL**: https://huggingface.co/datasets/cais/mmlu
- **Size**: 15,908 questions across 57 subjects
- **Relevant Subjects**: high_school_physics, high_school_chemistry, high_school_mathematics, college_physics, college_chemistry, college_mathematics
- **Solutions**: Correct answer labels (A/B/C/D)
- **Format**: CSV/JSON with question + 4 options + answer
- **JEE Relevance**: **MEDIUM-HIGH** - High school and college level physics/chemistry/math MCQs. Good breadth but lacks detailed solutions.

### 5.5 MMLU-Pro
- **URL**: https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro | https://github.com/TIGER-AI-Lab/MMLU-Pro
- **Size**: 12,000+ questions across 14 domains
- **Relevant Subjects**: Mathematics, Physics, Chemistry, Engineering
- **Solutions**: Correct answer labels (10 options per question)
- **Format**: JSON with question + 10 options
- **Paper**: NeurIPS 2024
- **JEE Relevance**: **MEDIUM-HIGH** - Harder than MMLU with more reasoning-focused questions.

---

## 6. SUMMARY: PRIORITY RANKING FOR JEE FINE-TUNING

### Tier 1 - MUST USE (Directly JEE-targeted or highly relevant)
| Dataset | Size | Why |
|---------|------|-----|
| JEEBench | 515 | Direct JEE Advanced questions with solutions |
| JEE-NEET Benchmark (Reja1) | Varies | Direct JEE/NEET with image-based questions |
| JEE/NEET JSON (Kaggle) | Varies | Direct JEE/NEET in structured JSON |
| OlympiadBench | 8,476 | Olympiad-level Math+Physics, expert annotations |
| NCERT Collection (KadamParth) | Textbooks | Foundational curriculum for JEE |

### Tier 2 - STRONGLY RECOMMENDED (High-quality, relevant subjects)
| Dataset | Size | Why |
|---------|------|-----|
| MATH (Hendrycks) | 12,500 | Competition math with step-by-step solutions |
| NuminaMath | 860,000 | Massive math with CoT solutions |
| AMPS | 5M+ (23GB) | Huge math pretraining corpus |
| SciBench | 789 | College-level PCM with detailed solutions |
| TheoremQA | 800 | Theorem-driven science problem solving |
| Math Olympiad (AoPS) | Large | Olympiad problems with solutions |

### Tier 3 - RECOMMENDED (Supplementary training data)
| Dataset | Size | Why |
|---------|------|-----|
| MMLU/MMLU-Pro (PCM subjects) | ~2k relevant | Standardized science MCQs |
| SciQ | 13,679 | Science MCQs with support text |
| ScienceQA | 21,000 | Multimodal science with explanations |
| MedMCQA | 194,000 | Medical entrance (NEET PG) questions |
| EXAMS-QA | 24,000 | Multi-subject high school exams |
| IITJEE NEET AIIMS (Kaggle) | Varies | Student questions data |

### Tier 4 - OPTIONAL (Lower relevance but useful)
| Dataset | Size | Why |
|---------|------|-----|
| ARC | 7,787 | Grade-school reasoning (too easy) |
| OpenBookQA | 6,000 | Elementary science reasoning |
| MathQA | 37,000 | Math word problems |

---

## 7. RECOMMENDED DOWNLOAD COMMANDS

```bash
# HuggingFace datasets (use datasets library)
pip install datasets

# JEEBench
git clone https://github.com/dair-iitd/jeebench.git

# OlympiadBench
git clone https://github.com/OpenBMB/OlympiadBench.git

# MATH dataset
git clone https://github.com/hendrycks/math.git

# SciBench
git clone https://github.com/mandyyyyii/scibench.git

# TheoremQA
git clone https://github.com/TIGER-AI-Lab/TheoremQA.git

# Python - load from HuggingFace
from datasets import load_dataset

jeebench = load_dataset("daman1209arora/jeebench")
jee_neet = load_dataset("Reja1/jee-neet-benchmark")
ncert_phy12 = load_dataset("KadamParth/NCERT_Physics_12th")
ncert_chem12 = load_dataset("KadamParth/NCERT_Chemistry_12th")
ncert_phy11 = load_dataset("KadamParth/NCERT_Physics_11th")
ncert_chem11 = load_dataset("KadamParth/NCERT_Chemistry_11th")
olympiad = load_dataset("Hothan/OlympiadBench")
math_ds = load_dataset("hendrycks/competition_math")
numina = load_dataset("AI-MO/NuminaMath-CoT")
sciq = load_dataset("allenai/sciq")
scienceqa = load_dataset("derek-thomas/ScienceQA")
mmlu = load_dataset("cais/mmlu", "high_school_physics")
theoremqa = load_dataset("TIGER-Lab/TheoremQA")
medmcqa = load_dataset("openlifescienceai/medmcqa")
exams = load_dataset("exams")

# Kaggle datasets (use kaggle CLI)
pip install kaggle
kaggle datasets download -d damerajee/jee-question-json-format
kaggle datasets download -d mrutyunjaybiswal/iitjee-neet-aims-students-questions-data
kaggle datasets download -d thedevastator/sciq-a-dataset-for-science-question-answering
kaggle datasets download -d jeromeblanchet/arc-ai2-reasoning-challenge
kaggle datasets download -d mathurinache/math-dataset
kaggle datasets download -d imbishal7/math-olympiad-problems-and-solutions-aops
kaggle datasets download -d kishanvavdara/aimo-olympiadbench-math-dataset
kaggle datasets download -d pateldhruvikiranbhai/ncert-dataset
```
