URVA: Logic-Enhanced Hallucination Auditing Framework for Large Language Models

Overview

URVA (Unified Reliability Verification and Auditing) is a research framework designed to evaluate and audit hallucination-related risks in Large Language Models (LLMs).

Unlike traditional evaluation approaches that focus primarily on accuracy, URVA introduces a reliability-oriented auditing pipeline that measures logical consistency, grounding quality, and faithfulness of model outputs.

The framework applies deterministic verification, logic-based consistency analysis, and certainty estimation to identify cases where a model may produce factually unsupported or logically inconsistent responses despite appearing correct under standard benchmark metrics.

⸻

Motivation

Large Language Models often generate responses that appear convincing while containing factual errors, unsupported claims, or logical inconsistencies.

Traditional benchmark metrics such as accuracy, Exact Match (EM), and F1 score do not always capture these reliability risks.

URVA was developed to provide a complementary auditing framework that focuses on:

* Hallucination containment
* Logical consistency verification
* Grounding assessment
* Reliability estimation
* Safety-oriented model evaluation

⸻

Key Contributions

Unified Auditing Pipeline

A deterministic evaluation pipeline that standardizes auditing across multiple hallucination and reasoning benchmarks.

Logic-Based Verification

Applies lightweight rule-based reasoning to identify:

* Negation conflicts
* Entity mismatches
* Numeric inconsistencies
* Unsupported assertions
* Dataset label violations

Grounding Analysis

Measures the extent to which model outputs remain supported by the provided evidence or source context.

Faithfulness Assessment

Evaluates whether generated responses remain faithful to the underlying information rather than introducing unsupported details.

Certainty Scoring

Introduces a reliability-oriented certainty formulation:

Certainty = (1 − L) × (αF + βG)

Where:

* L = Logic Penalty
* F = Faithfulness Score
* G = Grounding Score

This formulation suppresses confidence when logical inconsistencies are detected, even if lexical or semantic alignment appears strong.

⸻

Evaluated Benchmarks

URVA was evaluated across multiple hallucination and reasoning datasets:

* TruthfulQA
* HaluEval
* FEVER
* RAGTruth
* HotpotQA
* 2WikiMultiHopQA

These benchmarks cover:

* Hallucination detection
* Fact verification
* Faithfulness auditing
* Multi-hop reasoning
* Retrieval-augmented generation evaluation

⸻

System Architecture

The framework follows a modular execution pipeline:

1. Dataset normalization
2. Constrained prompt construction
3. Model inference
4. Output verification
5. Logic auditing
6. Grounding analysis
7. Faithfulness assessment
8. Certainty score fusion

This architecture allows consistent auditing across heterogeneous benchmarks while remaining model-agnostic.

⸻

Results

URVA demonstrates competitive performance across multiple benchmarks while revealing reliability gaps that are often hidden by conventional evaluation metrics.

A key finding of this work is the distinction between:

* Correctness
* Faithfulness
* Reliability

The framework highlights situations where model predictions achieve high benchmark scores but remain weakly grounded or logically inconsistent.

⸻

Research Impact

URVA contributes to ongoing research in:

* LLM Reliability
* Hallucination Detection
* AI Safety
* Trustworthy AI
* Explainable Evaluation Frameworks

The framework is designed to support safer deployment and more transparent assessment of large language models.

⸻

Future Work

* Expanded logical reasoning capabilities
* Additional contradiction detection modules
* Integration with Retrieval-Augmented Generation systems
* Real-time auditing for production LLM applications
* Enhanced certainty calibration methods

⸻

Research Status

Research manuscript completed.

This repository contains the implementation and experimental framework used in the study.

Paper status: Under Review / Research Preprint.

⸻

Author

Sara Altoom

Artificial Intelligence Student

Research Interests:
Large Language Models (LLMs) • NLP • AI Safety • Hallucination Detection • Trustworthy AI
