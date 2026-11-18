import json
import time
from pathlib import Path
from openai import OpenAI

MODELS = [
    "qwen3.5:2b-q4_K_M",
    "qwen3.5:4b-q4_K_M"
]

PROMPTS = [
    {
        "category": "factual",
        "prompt": "What causes tides on Earth? Answer in 2 sentences."
    },
    {
        "category": "reasoning",
        "prompt": "A train travels 120 km in 1.5 hours and then 80 km in 1 hour. What is its average speed for the entire journey? Explain briefly."
    },
    {
        "category": "summarization",
        "prompt": "Summarize this paragraph in one sentence: A company introduced flexible working hours to improve employee satisfaction. Workers could choose when to start their day, provided they completed their tasks and attended required meetings. After six months, productivity increased and employee turnover decreased."
    },
    {
        "category": "structured",
        "prompt": 'List three European capitals. Return ONLY valid JSON in this format: [{"city": "...", "country": "..."}].'
    },
    {
        "category": "code",
        "prompt": "Write a Python function that checks whether a number is prime. Return only Python code."
    },
    {
        "category": "instruction",
        "prompt": "Explain machine learning using exactly 3 bullet points. Each bullet must contain no more than 8 words."
    }
]

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    timeout=600
)

results = []

for model in MODELS:
    print(f"\nTesting model: {model}")

    for item in PROMPTS:
        print(f"Running: {item['category']}")

        start = time.perf_counter()

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": item["prompt"]}
            ],
            temperature=0.7,
            reasoning_effort="none",
            max_tokens=1024
        )

        elapsed = time.perf_counter() - start
        choice = response.choices[0]
        usage = response.usage

        tokens = usage.completion_tokens if usage else None

        result = {
            "model": model,
            "category": item["category"],
            "prompt": item["prompt"],
            "response": choice.message.content,
            "thinking": False,
            "finish_reason": choice.finish_reason,
            "time_seconds": round(elapsed, 2),
            "prompt_tokens": usage.prompt_tokens if usage else None,
            "completion_tokens": tokens,
            "tokens_per_second": round(tokens / elapsed, 2) if tokens else None,
            "quality_rating": None,
            "rating_note": ""
        }

        results.append(result)

        Path("benchmark_results.json").write_text(
            json.dumps(results, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        print("Time:", result["time_seconds"], "seconds")
        print("Speed:", result["tokens_per_second"], "tokens/sec")
        print("Finish reason:", choice.finish_reason)

        if not choice.message.content:
            print("WARNING: Empty model response!")

print("\nBenchmark completed!")
print("Results saved:", len(results))