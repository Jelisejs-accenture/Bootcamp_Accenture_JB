# Day 11 Local RAG - Agent Instructions

## Goal
Build a local RAG pipeline to answer questions using five PDF documents.

## Rules
- Use only local Ollama models for the RAG pipeline.
- Never send company documents to cloud AI services.
- Never commit API keys, .env, .venv, or chroma_db.
- All benchmarks and evaluation metrics must come from actual saved results.
- Do not invent model outputs or quality ratings.
- The student writes decision_log.md personally.
- Work one stage at a time and test before continuing.
- Do not modify previous bootcamp days.

## Commands
- Install dependencies: uv sync
- Ingest documents: uv run python ingest.py
- Run benchmarks: uv run python benchmark.py
- Run pipeline: uv run python pipeline.py

## Checks
- Verify that Ollama responds locally.
- Check that documents are indexed and searchable.
- Save actual results in benchmark_results.json and pipeline_outputs.json.
