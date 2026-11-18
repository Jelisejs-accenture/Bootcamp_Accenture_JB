# Day 11 — Local RAG Capstone

## Project Overview

This project implements a fully local Retrieval-Augmented Generation (RAG) system for answering questions using five internal NovaTech Solutions PDF documents.

The system retrieves relevant document excerpts and generates grounded answers with page-level citations using locally hosted language models.

## Technology Stack

- Python 3.12 and uv
- Ollama for local model inference
- Qwen3.5 2B (primary language model)
- Qwen3.5 4B (benchmark comparison)
- nomic-embed-text for local embeddings
- ChromaDB for vector storage
- pypdf for PDF text extraction
- LangChain text splitters for chunking
- OpenAI-compatible local Ollama API

## Documents

The system processes five PDF files:

1. company_handbook.pdf
2. meeting_notes.pdf
3. product_guide.pdf
4. quarterly_report_q1_2026.pdf
5. security_policy.pdf

Document location:
../capstone/day11_capstone/documents/

Company documents are processed locally and are not sent to cloud AI APIs.

## System Architecture

PDF Documents
    |
    v
PDF Text Extraction
    |
    v
Text Chunking
    |
    v
Local Embeddings (nomic-embed-text)
    |
    v
ChromaDB
    |
    v
Question Embedding + Similarity Search
    |
    v
Retrieved Document Context
    |
    v
Local Qwen Model
    |
    v
Grounded Answer + Citations

## Configuration

Main configuration is stored in config.py.

- Chunk size: 900 characters
- Chunk overlap: 150 characters
- Retrieval top-k: 4
- Embedding model: nomic-embed-text
- Main LLM: qwen3.5:2b-q4_K_M
- Ollama context length: 8192
- Reasoning effort: none

The application uses a local OpenAI-compatible endpoint:
http://localhost:11434/v1

## Running the Project

From the local-rag directory:

Install dependencies:

    uv sync

Ingest the five PDF documents:

    uv run python ingest.py

Test document retrieval:

    uv run python retrieve.py "What are the company's security requirements?"

Generate an answer:

    uv run python generate.py "What security assessments are required for vendors?"

Run the complete RAG pipeline:

    uv run python pipeline.py "What is required when vendors handle Restricted data?"

Run the local model benchmark:

    uv run python benchmark.py

Run evaluation:

    uv run python evaluate.py

Manually review generated answers:

    uv run python review.py

Note: Running benchmark.py again overwrites benchmark_results.json.
Existing evaluation questions are skipped by evaluate.py.

## Model Benchmark

Both Qwen models were tested using six prompts:
factual knowledge, reasoning, summarization, structured JSON,
code generation, and instruction following.

Measured total execution times:

- Qwen3.5 2B: 87.84 seconds
- Qwen3.5 4B: 149.85 seconds

Qwen 2B was approximately 1.7 times faster in this test.

Both models were tested on CPU. The primary model was selected
with local hardware constraints and inference speed in mind.

Detailed measurements and manually reviewed quality ratings
are stored in benchmark_results.json.

## RAG Evaluation

The evaluation dataset contains 15 questions:

- Easy: 5
- Medium: 5
- Hard: 3
- Unanswerable: 2

Manual evaluation results:

| Difficulty | Passed | Total |
|------------|--------|-------|
| Easy | 4 | 5 |
| Medium | 1 | 5 |
| Hard | 1 | 3 |
| Unanswerable | 2 | 2 |
| Total | 8 | 15 |

Overall strict pass rate: 53.33%.

The evaluation generated 14 responses with finish_reason=stop
and one response with finish_reason=length.

All two unanswerable questions were correctly rejected
without inventing unsupported facts.

## Observed Limitations

1. Broad questions sometimes retrieved incomplete document context.
2. The support section in product_guide.pdf was missed by semantic retrieval.
3. Multi-document questions sometimes produced incomplete or misleading answers.
4. The model occasionally mixed information from different policies.
5. Some responses contained incorrect citations or contradictory conclusions.
6. One response was truncated at the original 512-token generation limit.

A targeted retrieval experiment for meeting_notes.pdf successfully found
the relevant action-item sections, but the generated response still
contained repetition and reached the 1024-token limit.

Original evaluation results were preserved for comparison.

## Project Files

- config.py — central configuration
- ingest.py — PDF extraction, chunking, and indexing
- retrieve.py — semantic retrieval from ChromaDB
- generate.py — grounded answer generation
- pipeline.py — end-to-end RAG pipeline
- benchmark.py — local model comparison
- evaluate.py — evaluation execution
- review.py — manual answer review
- test_questions.json — evaluation questions and reference answers
- benchmark_results.json — model benchmark results
- pipeline_outputs.json — original RAG responses and manual ratings
- evaluation_summary.json — evaluation statistics
- decision_log.md — design decisions and observations
- AGENTS.md — development instructions

## Privacy

All LLM and embedding requests use the local Ollama server.
The ChromaDB database and Python virtual environment are excluded
from Git tracking.

The source PDFs must only be shared in an authorized repository.
