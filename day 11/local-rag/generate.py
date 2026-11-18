import time
import sys
from openai import OpenAI

from config import (
    LLM_BASE_URL,
    LLM_API_KEY,
    LLM_MODEL,
    TEMPERATURE,
    MAX_OUTPUT_TOKENS,
    TOKEN_LIMIT_PARAM,
)
from retrieve import retrieve


def generate_answer(question, chunks, model=LLM_MODEL):
    client = OpenAI(
        base_url=LLM_BASE_URL,
        api_key=LLM_API_KEY,
        timeout=600,
    )

    context = "\n\n".join(
        f"[Source: {c['source']}, page {c['page']}]\n{c['text']}"
        for c in chunks
    )

    system_prompt = """
You are a company document assistant.

Rules:
- Answer ONLY using the provided document excerpts.
- Do not invent facts or use outside knowledge.
- If the answer is not supported by the excerpts, say:
  "I could not find this information in the provided documents."
- Cite sources using [filename.pdf, p. X].
- Do not cite documents that do not support the answer.
- Keep the answer clear and concise.
"""

    user_prompt = f"""
DOCUMENT EXCERPTS:
{context}

QUESTION:
{question}
"""

    start = time.perf_counter()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=TEMPERATURE,
        reasoning_effort="none",
        **{TOKEN_LIMIT_PARAM: MAX_OUTPUT_TOKENS},
    )

    latency = time.perf_counter() - start
    choice = response.choices[0]
    usage = response.usage

    return {
        "question": question,
        "answer": choice.message.content or "",
        "model": model,
        "thinking": False,
        "finish_reason": choice.finish_reason,
        "prompt_tokens": usage.prompt_tokens if usage else None,
        "generated_tokens": usage.completion_tokens if usage else None,
        "latency_seconds": round(latency, 2),
        "retrieved_chunks": chunks,
    }


if __name__ == "__main__":
    question = " ".join(sys.argv[1:])

    if not question:
        question = "What security assessments are required for vendors?"

    chunks = retrieve(question)
    result = generate_answer(question, chunks)

    print("\nQUESTION:")
    print(question)

    print("\nGENERATED ANSWER:")
    print(result["answer"])

    print("\nMODEL:", result["model"])
    print("FINISH REASON:", result["finish_reason"])
    print("GENERATED TOKENS:", result["generated_tokens"])
    print("LATENCY:", result["latency_seconds"], "seconds")