# Day 11 Local RAG - Agent Instructions

## Goal
Build a local RAG system that answers questions using five PDF documents.

## Rules
- Use only local Ollama models in the RAG pipeline.
- Never upload company documents to cloud AI services.
- Never commit .env, .venv or chroma_db.
- Record actual measurements in JSON files.
- Do not invent benchmark results or quality ratings.
- The student writes the decision log personally.
- Complete and test one stage before starting another.
- Do not change files from previous bootcamp days.

## Commands
- Install dependencies: uv sync
- Ingest documents: uv run python ingest.py
- Run benchmark: uv run python benchmark.py
- Run pipeline: uv run python pipeline.py

## Checks
- Verify Ollama responds locally.
- Verify document ingestion and retrieval.
- Save real benchmark and pipeline results.
