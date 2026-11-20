# Day 13 — Agentic AI and ReAct Agents

This folder contains the original practical notebook with the missing exercises
implemented. `# Reason:` comments explain the choice behind each solution.

## Preparation

1. Open `Practice - Agentic AI and ReAct Agents completed.ipynb` in VS Code and select a Python Jupyter kernel.
2. Install dependencies into **that kernel's Python environment**:
   `python -m pip install -r requirements.txt`
3. Copy `.env.example` to `.env` in this folder. `.env` is excluded from Git by `.gitignore`.
4. For `OPENAI_ENDPOINT`, use the Azure OpenAI `/openai/v1/` base URL used in Day 8/12.
   For `OPENAI_MODEL`, use a model **deployment name** available to that Azure account. The example `gpt-5.4-mini` was used in previous Day 12 evaluations, but verify that it supports the Responses API and tool calls; otherwise use another accessible deployment.
5. The notebook tries to reuse your existing `OPENAI_API_KEY` from `../day 8/.env`.
   If absent, put the key only in local `.env` (never notebook source or Git).
6. Get a free Tavily API key at https://app.tavily.com/ and put it under `TAVILY_API_KEY` in `.env`.

## Run and verify

- Run from top to bottom using the notebook kernel with access to the `.env` file.
- Exercise 1 should print `5 is odd` and `8 is even`.
- The manual ReAct memory exercise should print `Final answer: 110`.
- The arithmetic ReAct exercise should answer `(100 + 50) * 2 / 3 = 100`.
- The Tavily section should answer the assigned question about today's weather in Latvia and Lithuania with source URLs, if current weather results are available.

## Security

Never commit `.env`, API keys, or raw credential output. Check the GitHub Desktop
changes list before publishing. `.env.example` contains placeholders only.

## Testing status

The notebook's code syntax, the first two exercises, and the ReAct and Tavily
integration logic were tested locally using mocked API responses. **Live
OpenAI/Azure and Tavily API calls have not yet been executed.**
