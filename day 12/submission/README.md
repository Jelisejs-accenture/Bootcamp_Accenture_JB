# Day 12 — Local RAG Evaluation

## Project

Evaluation of my Day 11 local document Q&A pipeline.

- Local model: qwen3.5:2b-q4_K_M
- Cloud comparison: gpt-5.6-luna
- DeepEval judge: gpt-5.4-mini
- DeepEval version: 4.3.4
- Test questions: 15
- Evaluation date: 19 November 2026

## Results

All five DeepEval metrics were calculated for both models.

The cloud model was significantly faster in this experiment,
but the paired evaluation did not establish a clear quality
advantage for either model.

Security testing included nine attacks per model,
with manually reviewed verdicts and explanations.

See evaluation_report.md for detailed findings and recommendations.
See comparison_output.md for the numerical comparison.

## Files

- eval_pipeline.py: provided DeepEval evaluation script
- security_probe.py: security probes with two additional attacks
- compare.py: statistical comparison with 2x standard error
- run_day12_cloud.py: cloud generation runner
- pipeline_outputs_*.json: model outputs
- eval_results_*.json: DeepEval results
- security_results_*.json: security tests and reviewed verdicts
- comparison_output.md: comparison output
- evaluation_report.md: findings and recommendations

## Reproduction

The original runnable pipeline and its dependencies are located
in day 11/local-rag, relative to the repository root.

The evaluation and security scripts were run from that project
directory, where retrieve.py, generate.py, config.py and
ChromaDB are available.

Commands used from the Day 11 local-rag directory:

    uv run python eval_pipeline.py local
    uv run python eval_pipeline.py cloud
    uv run python compare.py
    uv run python security_probe.py local
    uv run python security_probe.py cloud

Cloud runs require authorized Azure API credentials.
The LLM_* environment variables select the cloud generator.
Embeddings and ChromaDB retrieval remain local.

Never commit API keys, .env, .venv or chroma_db.

## AI assistance

OpenAI ChatGPT was used to assist with Python scripts,
debugging, calculations and organizing the evaluation.
The models were executed and their outputs collected locally
or through the configured Azure endpoint.

