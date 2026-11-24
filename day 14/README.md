# Day 14 — fast local final challenges (Ollama)

These **five short notebooks** implement the five **final challenges** from the uploaded Day 14 training notebooks:

1. smolagents: Smart Home Controller
2. LangGraph: Travel Assistant
3. LlamaIndex: Restaurant Recommendation Agent (mock data, no real booking)
4. Google ADK: Nutrition Calculator (illustrative food data)
5. CrewAI: Movie Casting Assistant (fictional actors)

The original lecture demonstrations are **not repeated** in these short versions. If the teacher expects every demonstration cell, keep the original uploaded notebooks as well.

## Start

1. Make sure Ollama is running: `ollama list`.
2. Open each notebook in VS Code with a Python kernel.
3. Execute cells top to bottom. The first run has `RUN_AGENT=False`, so all deterministic tests complete without API calls or slow model generation.
4. In the **shared settings cell**, set `RUN_AGENT=True` and rerun that cell and the last agent cell to obtain an actual local-model agent trace. It can be slow on small Qwen models.
5. For more reliable tool use, set `MODEL_NAME = "qwen3.5:4b-q4_K_M"` (installed on the user's computer), at the cost of speed and memory.
6. Save notebooks with the observed outputs before submission; only an actual run verifies model behavior.

## What has been checked

- Every notebook passes notebook format validation and Python parsing of every code cell.
- Every notebook has a deterministic tool-test section with assertions and a separate model-run section.
- Model endpoints use only `http://127.0.0.1:11434`, not Azure/OpenAI cloud.
- Does **not** need `.env` or a purchased API key.
- Framework import/API compatibility and the actual agent calls **cannot be established in this execution environment**, because these five frameworks and your local Ollama model are not installed here. If `RUN_AGENT=True` fails, use the traceback to identify the framework-specific issue. Do not report a model result as passed without running it.

## Risk / submission

This is a **local adaptation**, while the original coursework specifies Azure OpenAI. Ask the instructor whether Ollama is allowed. The project is public-facing on GitHub: never commit `.env`, private documents, tokens, or confidential client information. The mock restaurant and actor data are fictional.
