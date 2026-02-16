# Comprehensive Dataset Report for IIT JEE Model Training
## Class 12 Level Physics, Chemistry, and Mathematics

Generated: 2026-02-15

---

## TABLE OF CONTENTS

1. [TIER 1: JEE/NEET-Specific Datasets](#tier-1)
2. [TIER 2: Large Math Reasoning Datasets (with CoT)](#tier-2)
3. [TIER 3: Physics Datasets](#tier-3)
4. [TIER 4: Chemistry Datasets](#tier-4)
5. [TIER 5: General Science & STEM Datasets](#tier-5)
6. [TIER 6: Large-Scale Pretraining Corpora](#tier-6)
7. [TIER 7: Indian Education / NCERT Datasets](#tier-7)
8. [Summary & Recommendations](#summary)

---

## TIER 1: JEE/NEET-SPECIFIC DATASETS <a name="tier-1"></a>

### 1. JEEBench (daman1209arora/jeebench)
- **URL**: https://huggingface.co/datasets/daman1209arora/jeebench
- **Size**: 515 problems
- **Subjects**: Physics, Chemistry, Mathematics
- **Source**: IIT JEE Advanced 2016-2023
- **Format**: MCQ (single), MCQ (multiple correct), Integer type
- **Solutions**: Correct answers only (gold field) -- NO step-by-step solutions
- **Data Fields**: subject, description, question (LaTeX), gold, type, index
- **License**: MIT
- **Quality**: HIGH -- Published at EMNLP 2023. Curated from real JEE Advanced papers. GPT-4 achieves <40% accuracy.
- **Limitations**: Small dataset (only 515 problems). No detailed solutions.
- **Best Use**: Evaluation benchmark, not training data.

### 2. PhysicsWallahAI/JEE-Main-2025-Math
- **URL**: https://huggingface.co/datasets/PhysicsWallahAI/JEE-Main-2025-Math
- **Size**: 475 questions
- **Subjects**: Mathematics only
- **Source**: Official JEE Mains 2025 (January + April sessions)
- **Format**: MCQ and numerical
- **Solutions**: Answer keys cross-verified with NTA. No step-by-step solutions.
- **License**: Not specified
- **Quality**: HIGH -- Official exam questions with verified answers.
- **Best Use**: Evaluation benchmark for math.

### 3. CK0607/2025-Jee-Mains-Question
- **URL**: https://huggingface.co/datasets/CK0607/2025-Jee-Mains-Question
- **Size**: 250 questions
- **Subjects**: Mathematics only
- **Source**: JEE Main 2025 (4 shifts)
- **Format**: MCQ with correct option number (1-4)
- **Solutions**: Correct option number only. NO explanations.
- **Data Fields**: unique_id, Shift_Name, Subject, Question_Number, Question_Text, Correct_Option
- **License**: Apache 2.0
- **Quality**: MEDIUM -- Useful but small and math-only.

### 4. Reja1/jee-neet-benchmark
- **URL**: https://huggingface.co/datasets/Reja1/jee-neet-benchmark
- **Size**: 576 questions
- **Subjects**: Physics, Chemistry, Mathematics (JEE), Botany, Zoology (NEET)
- **Source**: JEE Advanced 2024-2025, NEET 2024-2025
- **Format**: IMAGE-based (PNG). MCQ single, MCQ multiple, Integer type.
- **Solutions**: Correct answers only. NO step-by-step solutions.
- **Data Fields**: image, question_id, exam_name, exam_year, subject, question_type, correct_answer
- **License**: MIT
- **Quality**: MEDIUM-HIGH -- Authentic exam papers but IMAGE format (requires multimodal model). No text extraction.
- **Limitation**: Questions are images, not text. Requires OCR or multimodal model.

### 5. Kaggle: JEE AND NEET QUESTION JSON FORMAT
- **URL**: https://www.kaggle.com/datasets/damerajee/jee-question-json-format
- **Size**: Unknown (requires Kaggle access)
- **Subjects**: Physics, Chemistry, Mathematics
- **Format**: JSON
- **Quality**: MEDIUM -- Community-contributed.

### 6. Kaggle: IITJEE NEET AIIMS Students Questions Data
- **URL**: https://www.kaggle.com/datasets/mrutyunjaybiswal/iitjee-neet-aims-students-questions-data
- **Size**: Unknown (requires Kaggle access)
- **Subjects**: Multiple competitive exam subjects
- **Quality**: MEDIUM -- Community-contributed.

---

## TIER 2: LARGE MATH REASONING DATASETS (with Chain-of-Thought) <a name="tier-2"></a>

### 7. NuminaMath-CoT (AI-MO/NuminaMath-CoT) *** HIGHLY RECOMMENDED ***
- **URL**: https://huggingface.co/datasets/AI-MO/NuminaMath-CoT
- **Size**: ~860,000 problems (859,594 rows, 1.23 GB)
- **Subjects**: Mathematics (algebra, geometry, calculus, number theory, combinatorics, trigonometry, olympiad)
- **Sources**: Chinese high school math, US/international olympiad problems, online exam PDFs, math forums
- **Format**: Problem + Chain-of-Thought solution
- **Solutions**: YES -- Every problem has a detailed CoT solution (13-10,400 chars)
- **Data Fields**: source, problem, solution, messages (chat format)
- **License**: Apache 2.0
- **Quality**: VERY HIGH -- Created by the team that won AIMO competition. Excellent for training.
- **Best Use**: PRIMARY training dataset for mathematics. Chain-of-thought format is ideal for fine-tuning.

### 8. NuminaMath-1.5 (AI-MO/NuminaMath-1.5)
- **URL**: https://huggingface.co/datasets/AI-MO/NuminaMath-1.5
- **Size**: ~896,215 rows (531 MB)
- **Subjects**: Competition-level mathematics
- **Format**: Problem + solution pairs
- **Solutions**: YES
- **License**: Apache 2.0
- **Quality**: VERY HIGH -- Upgraded version of NuminaMath.

### 9. OpenMathReasoning (nvidia/OpenMathReasoning) *** HIGHLY RECOMMENDED ***
- **URL**: https://huggingface.co/datasets/nvidia/OpenMathReasoning
- **Size**: 306K unique problems; CoT split: 3.2M examples; TIR split: 1.7M examples
- **Subjects**: Mathematics (competition-level, sourced from AoPS forums)
- **Format**: Problem + generated solution + expected answer
- **Solutions**: YES -- Multiple solution traces per problem generated by DeepSeek-R1 and QwQ-32B
- **Data Fields**: problem, generated_solution, problem_type, expected_answer
- **License**: CC-BY-4.0
- **Quality**: VERY HIGH -- Won NVIDIA the AIMO-2 Kaggle competition. Multiple verified solutions per problem.
- **Best Use**: Excellent for training mathematical reasoning. Multiple solutions enable DPO/rejection sampling.

### 10. OpenR1-Math-220k (open-r1/OpenR1-Math-220k)
- **URL**: https://huggingface.co/datasets/open-r1/OpenR1-Math-220k
- **Size**: ~225,129 problems with 2-4 reasoning traces each
- **Subjects**: Mathematics
- **Sources**: NuminaMath 1.5 problems solved by DeepSeek R1
- **Format**: Problem + multiple reasoning traces + verification
- **Solutions**: YES -- Long step-by-step reasoning (up to 16K tokens per solution)
- **Data Fields**: problem, solution, answer, problem_type, question_type, source, generations, correctness_math_verify
- **License**: Apache 2.0
- **Quality**: VERY HIGH -- From HuggingFace's Open R1 project. Verified solutions.

### 11. MATH Dataset (hendrycks/competition_math)
- **URL**: https://huggingface.co/datasets/hendrycks/competition_math
- **Size**: 12,500 problems
- **Subjects**: Mathematics (AMC 10, AMC 12, AIME, etc.)
- **Topics**: Algebra, Counting & Probability, Geometry, Intermediate Algebra, Number Theory, Prealgebra, Precalculus
- **Format**: Problem + full step-by-step solution in LaTeX
- **Solutions**: YES -- Complete step-by-step solutions with final answer in \boxed{}
- **Difficulty Levels**: 1-5
- **License**: MIT
- **Quality**: VERY HIGH -- Gold standard math reasoning benchmark. Used everywhere.
- **Best Use**: Core training dataset for competition math.

### 12. MetaMathQA (meta-math/MetaMathQA)
- **URL**: https://huggingface.co/datasets/meta-math/MetaMathQA
- **Size**: 395,000 question-answer pairs
- **Subjects**: Mathematics (augmented from GSM8K and MATH)
- **Format**: Forward and reverse augmented math QA pairs
- **Solutions**: YES -- Generated by LLM
- **Quality**: HIGH -- Augmented data proven to improve math reasoning.

### 13. GSM8K (openai/gsm8k)
- **URL**: https://huggingface.co/datasets/openai/gsm8k
- **Size**: 8,500 problems
- **Subjects**: Grade school mathematics
- **Format**: Word problems + multi-step solutions with calculator annotations
- **Solutions**: YES -- Detailed step-by-step reasoning
- **Quality**: HIGH -- Standard benchmark. Slightly below JEE level but good for building foundational reasoning.

### 14. Orca Math Word Problems (microsoft/orca-math-word-problems-200k)
- **URL**: https://huggingface.co/datasets/microsoft/orca-math-word-problems-200k
- **Size**: 200,035 problems
- **Subjects**: Grade school mathematics
- **Format**: Question + answer (generated by GPT-4 Turbo)
- **Solutions**: YES
- **Quality**: HIGH -- Large scale, GPT-4 quality answers. Below JEE level difficulty.

### 15. OpenThoughts3-1.2M (open-thoughts/OpenThoughts3-1.2M)
- **URL**: https://huggingface.co/datasets/open-thoughts/OpenThoughts3-1.2M
- **Size**: 1.2M problems (850K math + 250K code + 100K science)
- **Subjects**: Mathematics, Science, Code
- **Format**: Problem + reasoning traces (generated by QwQ-32B)
- **Solutions**: YES -- Long reasoning traces
- **Quality**: VERY HIGH -- #1 trending dataset on HuggingFace. Result of 1000+ curation experiments.
- **Best Use**: The science subset (100K) is especially valuable for physics/chemistry reasoning.

### 16. Olympiad Math Stepwise Solutions (kevin009/olympiad-math-stepwise-solutions-llama3-20k)
- **URL**: https://huggingface.co/datasets/kevin009/olympiad-math-stepwise-solutions-llama3-20k
- **Size**: 20,300 problems
- **Subjects**: Mathematics (AMC, AIME -- algebra, number theory, geometry, precalculus)
- **Format**: Problem + stepwise solutions
- **Solutions**: YES -- Step-by-step
- **Quality**: HIGH -- Competition math at JEE-relevant difficulty.

### 17. MathQA (allenai/math_qa)
- **URL**: https://huggingface.co/datasets/allenai/math_qa
- **Size**: ~37,000 problems
- **Subjects**: Mathematics (annotated from AQuA-RAT)
- **Format**: MCQ with operational programs
- **Solutions**: YES -- Operational program annotations
- **Quality**: MEDIUM-HIGH

---

## TIER 3: PHYSICS DATASETS <a name="tier-3"></a>

### 18. CAMEL-AI Physics (camel-ai/physics)
- **URL**: https://huggingface.co/datasets/camel-ai/physics
- **Size**: 20,000 problem-solution pairs
- **Subjects**: Physics (25 topics x 25 subtopics x 32 problems)
- **Format**: Problem + detailed solution (generated by GPT-4)
- **Solutions**: YES -- Full solutions in message_2 field
- **Data Fields**: role_1, topic, sub_topic, message_1 (problem), message_2 (solution)
- **Quality**: HIGH -- GPT-4 generated, covers wide range of physics topics.
- **Best Use**: Good training data for physics reasoning.

### 19. PhysReason (zhibei1204/PhysReason)
- **URL**: https://huggingface.co/datasets/zhibei1204/PhysReason
- **Size**: 1,200 problems
- **Subjects**: Physics (147 theorems, multiple domains)
- **Format**: Problem + multi-step solution (avg 8.1 steps, up to 15.6 for hard)
- **Solutions**: YES -- Step-by-step with theorem application
- **Difficulty**: Knowledge, Easy, Medium, Hard
- **Quality**: VERY HIGH -- Comprehensive benchmark. 81% include diagrams.
- **Limitation**: Relatively small. Best for evaluation + selective training.

### 20. PhysUniBench (PrismaX/PhysUniBench)
- **URL**: https://huggingface.co/datasets/PrismaX/PhysUniBench
- **Size**: 3,304 problems
- **Subjects**: Physics (undergraduate-level)
- **Format**: Multimodal (image + text)
- **Solutions**: YES -- With visual reasoning
- **Quality**: HIGH -- First large-scale multimodal physics benchmark for undergrad level.

### 21. SciBench (xw27/scibench)
- **URL**: https://huggingface.co/datasets/xw27/scibench
- **Size**: 695 problems (open set)
- **Subjects**: Physics, Chemistry, Mathematics (college-level textbooks)
- **Format**: Open-ended, free-response
- **Solutions**: YES -- Multi-step solutions
- **Quality**: HIGH -- From actual college textbooks. Requires multi-step reasoning.

---

## TIER 4: CHEMISTRY DATASETS <a name="tier-4"></a>

### 22. CAMEL-AI Chemistry (camel-ai/chemistry)
- **URL**: https://huggingface.co/datasets/camel-ai/chemistry
- **Size**: 20,000 problem-solution pairs
- **Subjects**: Chemistry (25 topics x 25 subtopics x 32 problems)
- **Format**: Problem + solution (generated by GPT-4)
- **Solutions**: YES
- **Quality**: HIGH -- Wide topic coverage, GPT-4 quality.
- **Best Use**: Good training data for chemistry reasoning.

### 23. ChemBench (jablonkagroup/ChemBench)
- **URL**: https://huggingface.co/datasets/jablonkagroup/ChemBench
- **Size**: 2,700+ questions
- **Subjects**: Inorganic, organic, physical chemistry, materials science
- **Topics**: Coordination chemistry, organometallics, reaction mechanisms, stereochemistry
- **Format**: MCQ + open-ended reasoning
- **Solutions**: Expert-curated answers
- **Quality**: VERY HIGH -- Curated by domain experts.

### 24. ChemPile-Education (jablonkagroup/chempile-education)
- **URL**: https://huggingface.co/datasets/jablonkagroup/chempile-education
- **Size**: 58,946 documents, 114M tokens
- **Subjects**: General chemistry, organic chemistry, inorganic chemistry, physical chemistry, biochemistry
- **Format**: Educational text (undergrad to graduate level)
- **Solutions**: Conceptual explanations
- **License**: CC-BY-SA-4.0
- **Quality**: HIGH -- Good for pretraining on chemistry knowledge.

### 25. ChemPile-Reasoning (jablonkagroup/chempile-reasoning)
- **URL**: https://huggingface.co/datasets/jablonkagroup/chempile-reasoning
- **Size**: 10K-100K examples
- **Subjects**: Chemistry reasoning
- **Sources**: Stack Exchange, SOTA model reasoning traces
- **Format**: Instruction + reasoning
- **Quality**: HIGH -- Specifically for chemistry reasoning tasks.

### 26. ChemistryQA (avaliev/ChemistryQA)
- **URL**: https://huggingface.co/datasets/avaliev/ChemistryQA
- **Size**: ~4,500 questions
- **Subjects**: ~200 chemistry topics
- **Source**: Socratic.org
- **Format**: Q&A
- **Quality**: MEDIUM

### 27. ChemPref-DPO (AI4Chem/ChemPref-DPO-for-Chemistry-data-en)
- **URL**: https://huggingface.co/datasets/AI4Chem/ChemPref-DPO-for-Chemistry-data-en
- **Subjects**: Chemistry
- **Format**: DPO preference pairs
- **Quality**: HIGH -- Useful for preference/alignment training on chemistry.

### 28. ChemQA (shangzhu/ChemQA)
- **URL**: https://huggingface.co/datasets/shangzhu/ChemQA
- **Subjects**: Chemistry reasoning
- **Format**: Multimodal Q&A
- **Quality**: MEDIUM-HIGH

### 29. ChemData700K (daichira/ChemData700K_preprocess_added_chem_reasoning)
- **URL**: https://huggingface.co/datasets/daichira/ChemData700K_preprocess_added_chem_reasoning
- **Size**: ~700K
- **Subjects**: Chemistry with added reasoning
- **Quality**: MEDIUM-HIGH -- Large scale.

---

## TIER 5: GENERAL SCIENCE & STEM DATASETS <a name="tier-5"></a>

### 30. SciInstruct (zd21/SciInstruct)
- **URL**: https://huggingface.co/datasets/zd21/SciInstruct
- **Size**: 91,800 examples
- **Subjects**: Mathematics, Physics, Chemistry (+ formal proofs)
- **Format**: content (problem) + summary (detailed solution/explanation)
- **Solutions**: YES -- Detailed step-by-step with scientific concept analysis
- **License**: CC-BY-4.0
- **Quality**: HIGH -- Published at NeurIPS 2024. Self-reflective annotation process.
- **Note**: Primarily Chinese mathematical problems with solutions. Covers undergrad to graduate level.
- **Best Use**: Excellent multi-subject training data with solutions.

### 31. ScienceQA (derek-thomas/ScienceQA)
- **URL**: https://huggingface.co/datasets/derek-thomas/ScienceQA
- **Size**: 21,200 questions (12.7K train, 4.24K val, 4.24K test)
- **Subjects**: Physics, Chemistry, Biology, Earth Science (26 topics, 127 categories)
- **Format**: Multimodal MCQ with lectures and explanations
- **Solutions**: YES -- Lectures + explanations for answers
- **License**: CC-BY-SA-4.0
- **Quality**: HIGH -- Well-structured with explanations. Elementary to high school level.

### 32. SciQ (allenai/sciq)
- **URL**: https://huggingface.co/datasets/allenai/sciq
- **Size**: 13,679 questions
- **Subjects**: Physics, Chemistry, Biology
- **Format**: MCQ (4 options) + supporting evidence paragraph
- **Solutions**: Supporting evidence paragraph for correct answer
- **License**: CC-BY-NC-3.0
- **Quality**: MEDIUM-HIGH -- Crowdsourced science exam questions.

### 33. GPQA (Idavidrein/gpqa)
- **URL**: https://huggingface.co/datasets/Idavidrein/gpqa
- **Size**: 448 questions
- **Subjects**: Biology, Physics, Chemistry (graduate-level)
- **Format**: MCQ
- **Solutions**: Expert explanations
- **Quality**: VERY HIGH -- Graduate-level, "Google-proof". Written by PhD experts.
- **Limitation**: Very small. Best for evaluation only.

### 34. TheoremQA (TIGER-Lab/TheoremQA)
- **URL**: https://huggingface.co/datasets/TIGER-Lab/TheoremQA
- **Size**: 800 QA pairs covering 350+ theorems
- **Subjects**: Math (442), Physics (131), CS&EE (146), Finance (81)
- **Format**: Q&A, some with image input
- **Solutions**: Theorem-driven solutions
- **Quality**: HIGH -- University-level, expert-curated.

### 35. MMLU-Pro (TIGER-Lab/MMLU-Pro)
- **URL**: https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro
- **Size**: 12,000+ questions
- **Subjects**: 14 domains including Physics, Chemistry, Math, Biology, Engineering
- **Format**: MCQ (10 choices)
- **Solutions**: Correct answers, some with explanations
- **Quality**: HIGH -- Enhanced version of MMLU with STEM questions from TheoremQA and SciBench.

### 36. ARC - AI2 Reasoning Challenge (allenai/ai2_arc)
- **URL**: https://huggingface.co/datasets/allenai/ai2_arc
- **Size**: 7,787 questions
- **Subjects**: Science (grade-school level)
- **Format**: MCQ + 14M science sentence corpus
- **Quality**: MEDIUM -- Below JEE level but useful for foundational science.

### 37. MedMCQA (openlifescienceai/medmcqa)
- **URL**: https://huggingface.co/datasets/openlifescienceai/medmcqa
- **Size**: 194,000+ questions
- **Subjects**: Medical sciences (21 subjects, 2,400 healthcare topics)
- **Source**: AIIMS & NEET PG entrance exams
- **Format**: MCQ
- **Solutions**: Explanations for many questions
- **Quality**: HIGH -- Large-scale Indian competitive medical exam dataset.
- **Relevance**: Relevant for chemistry/biology at competitive exam level. NEET-adjacent.

---

## TIER 6: LARGE-SCALE PRETRAINING CORPORA <a name="tier-6"></a>

### 38. FineMath (HuggingFaceTB/finemath) *** RECOMMENDED FOR PRETRAINING ***
- **URL**: https://huggingface.co/datasets/HuggingFaceTB/finemath
- **Size**: 34B tokens (FineMath-3+) / 9.6B tokens (FineMath-4+)
- **Subjects**: Mathematics
- **Format**: Web-extracted math content in Markdown + LaTeX
- **Quality**: VERY HIGH -- Best public math pretraining dataset. Carefully filtered from Common Crawl.
- **Best Use**: Continued pretraining to build math foundation.

### 39. OpenWebMath (open-web-math/open-web-math)
- **URL**: https://huggingface.co/datasets/open-web-math/open-web-math
- **Size**: 6.3M documents, 14.7B tokens
- **Subjects**: Mathematics, Physics, Statistics, Computer Science
- **Sources**: 130K+ domains including forums, educational pages, blogs
- **Format**: Web text (filtered for math content)
- **License**: ODC-By 1.0
- **Quality**: HIGH -- Well-filtered mathematical web content.

### 40. MathPile (GAIR/MathPile)
- **URL**: https://huggingface.co/datasets/GAIR/MathPile
- **Size**: ~9.5 billion tokens
- **Sources**: Textbooks, arXiv, Wikipedia, ProofWiki, StackExchange, Web pages
- **Format**: Diverse math text
- **Quality**: HIGH -- Wide range of math sources.

### 41. InfiMM-WebMath-40B (Infi-MM/InfiMM-WebMath-40B)
- **URL**: https://huggingface.co/datasets/Infi-MM/InfiMM-WebMath-40B
- **Size**: 24M web pages, 85M images, 40B text tokens
- **Subjects**: Mathematics (multimodal)
- **Format**: Web pages with images + text
- **Quality**: HIGH -- Multimodal math pretraining data.

### 42. DeepMind Math Dataset (deepmind/math_dataset)
- **URL**: https://huggingface.co/datasets/deepmind/math_dataset
- **Size**: 2M QA pairs per module (~125 GB total)
- **Subjects**: Algebra, Arithmetic, Calculus, Comparison, Measurement, Numbers, Polynomials, Probability
- **Format**: Short question + short answer (160 chars / 30 chars)
- **Quality**: HIGH -- Programmatically generated. Good for building computational skills.
- **Limitation**: School-level difficulty. No step-by-step solutions.

### 43. ChemPile-Education (jablonkagroup/chempile-education)
- **URL**: https://huggingface.co/datasets/jablonkagroup/chempile-education
- **Size**: 58,946 documents, 114M tokens
- **Subjects**: All branches of chemistry
- **Quality**: HIGH -- Chemistry-specific pretraining data.

---

## TIER 7: INDIAN EDUCATION / NCERT DATASETS <a name="tier-7"></a>

### 44. NCERT Dataset (KadamParth/Ncert_dataset) *** HIGHLY RELEVANT ***
- **URL**: https://huggingface.co/datasets/KadamParth/Ncert_dataset
- **Size**: 120,406 rows (107 MB)
- **Subjects**: 13 subjects including Physics, Chemistry, Biology, Mathematics
- **Grades**: 6 through 12
- **Format**: Question + Answer + Explanation
- **Data Fields**: Topic, Explanation, Question, Answer, Difficulty (Easy/Medium/Hard), StudentLevel, QuestionType, QuestionComplexity (0-10), Prerequisites, EstimatedTime, subject, grade
- **License**: MIT
- **Quality**: MEDIUM-HIGH -- Large, well-structured NCERT-aligned dataset with difficulty levels.
- **Best Use**: Core dataset for NCERT/CBSE content. Filter for grade 11-12 Physics, Chemistry, Math.

### 45. NCERT Physics 12th (KadamParth/NCERT_Physics_12th)
- **URL**: https://huggingface.co/datasets/KadamParth/NCERT_Physics_12th
- **Subjects**: Physics (Class 12)
- **Quality**: MEDIUM-HIGH -- Subject-specific NCERT content.

### 46. NCERT Chemistry 12th (KadamParth/NCERT_Chemistry_12th)
- **URL**: https://huggingface.co/datasets/KadamParth/NCERT_Chemistry_12th
- **Subjects**: Chemistry (Class 12)
- **Quality**: MEDIUM-HIGH

### 47. NCERT Chemistry 11th (KadamParth/NCERT_Chemistry_11th)
- **URL**: https://huggingface.co/datasets/KadamParth/NCERT_Chemistry_11th
- **Subjects**: Chemistry (Class 11)
- **Quality**: MEDIUM-HIGH

### 48. Science Class 11 Textbook (dmedhi/science-class11-textbook)
- **URL**: https://huggingface.co/datasets/dmedhi/science-class11-textbook
- **Subjects**: Physics, Chemistry (Class 11 textbook content)
- **Format**: Chapter text content
- **Quality**: MEDIUM -- Raw textbook content, useful for pretraining.

### 49. NPTEL Dataset (ai4bharat/NPTEL)
- **URL**: https://huggingface.co/datasets/ai4bharat/NPTEL
- **Subjects**: Various engineering/science topics (from IIT lectures)
- **Format**: Lecture transcripts
- **Quality**: HIGH -- From actual IIT NPTEL courses.

---

## SUMMARY & RECOMMENDATIONS <a name="summary"></a>

### Recommended Training Pipeline

#### Phase 1: Continued Pretraining (Knowledge Building)
| Dataset | Tokens/Size | Purpose |
|---------|-------------|---------|
| FineMath-3+ | 34B tokens | Math foundation |
| OpenWebMath | 14.7B tokens | Math + Physics web content |
| MathPile | 9.5B tokens | Diverse math sources |
| ChemPile-Education | 114M tokens | Chemistry knowledge |

#### Phase 2: Supervised Fine-Tuning (Problem Solving)
| Dataset | Examples | Purpose | Priority |
|---------|----------|---------|----------|
| **NuminaMath-CoT** | **860K** | **Math CoT reasoning** | **CRITICAL** |
| **OpenMathReasoning** | **306K problems, 3.2M solutions** | **Math reasoning** | **CRITICAL** |
| **OpenR1-Math-220k** | **225K** | **Deep math reasoning** | **HIGH** |
| **OpenThoughts3-1.2M (science subset)** | **100K science** | **Science reasoning** | **HIGH** |
| **KadamParth/Ncert_dataset** | **120K** | **NCERT alignment** | **HIGH** |
| CAMEL-AI Physics | 20K | Physics problems | HIGH |
| CAMEL-AI Chemistry | 20K | Chemistry problems | HIGH |
| SciInstruct | 91.8K | Multi-subject science | HIGH |
| MATH (hendrycks) | 12.5K | Competition math | HIGH |
| MetaMathQA | 395K | Augmented math | MEDIUM |
| ChemPile-Reasoning | 10K-100K | Chemistry reasoning | MEDIUM |
| Orca Math 200K | 200K | Word problems | MEDIUM |

#### Phase 3: Evaluation Benchmarks
| Dataset | Examples | Purpose |
|---------|----------|---------|
| JEEBench | 515 | JEE Advanced eval |
| PhysicsWallahAI JEE-Main-2025 | 475 | JEE Main eval |
| Reja1/jee-neet-benchmark | 576 | JEE + NEET eval |
| GPQA | 448 | Graduate-level science eval |
| PhysReason | 1,200 | Physics reasoning eval |
| ChemBench | 2,700 | Chemistry eval |
| TheoremQA | 800 | STEM theorem eval |

### Total Estimated Training Data Available
- **Mathematics**: ~2M+ problems with solutions (NuminaMath + OpenMathReasoning + OpenR1 + MATH + MetaMath + Orca)
- **Physics**: ~25K problems with solutions (CAMEL + PhysReason + SciBench + OpenThoughts science subset)
- **Chemistry**: ~45K-750K problems (CAMEL + ChemBench + ChemPile-Reasoning + ChemData700K)
- **NCERT-aligned**: ~120K QA pairs across all subjects
- **Pretraining data**: ~60B+ tokens of math/science content

### Key Gaps Identified
1. **No large-scale JEE-specific dataset with step-by-step solutions exists** -- This is the biggest gap. The JEE-specific datasets are small (500-600 problems) and lack detailed solutions.
2. **Physics datasets are significantly smaller than math datasets** -- Physics reasoning data is ~10-50x smaller than math data.
3. **Chemistry datasets lack competition-level problem-solving** -- Most chemistry datasets are conceptual rather than computation-heavy.
4. **No single dataset covers all three JEE subjects with solutions** -- You will need to combine multiple datasets.

### Suggested Custom Data Creation
To fill the gaps, consider:
1. Scraping JEE/NEET PYQs from sites like ExamSIDE, MathonGo, Vedantu (with solutions)
2. Using GPT-4/Claude to generate step-by-step solutions for the 515 JEEBench problems
3. Augmenting NCERT dataset with competition-level variants
4. Creating synthetic JEE-style problems from the CAMEL-AI physics/chemistry data
