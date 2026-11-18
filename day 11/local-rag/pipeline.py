
import json
import re
import sys
import time

from config import BASE_DIR
from retrieve import retrieve
from generate import generate_answer


OUTPUT_FILE = BASE_DIR / "pipeline_outputs.json"


def run_pipeline(question):
    start = time.perf_counter()

    retrieval_start = time.perf_counter()
    chunks = retrieve(question)
    retrieval_time = time.perf_counter() - retrieval_start

    result = generate_answer(question, chunks)

    result["retrieval_latency_seconds"] = round(retrieval_time, 2)
    result["total_latency_seconds"] = round(
        time.perf_counter() - start, 2
    )

    citations = re.findall(
        r"\[([^\[\]]+?\.pdf),\s*(?:p\.|page)\s*(\d+)\]",
        result["answer"],
        flags=re.IGNORECASE,
    )

    result["citations"] = [
        {"source": source, "page": int(page)}
        for source, page in dict.fromkeys(citations)
    ]

    result["passed"] = None
    result["rating_note"] = ""

    return result


def main():
    question = " ".join(sys.argv[1:]).strip()

    if not question:
        print('Usage: uv run python pipeline.py "Your question"')
        return

    if OUTPUT_FILE.exists():
        results = json.loads(
            OUTPUT_FILE.read_text(encoding="utf-8")
        )
    else:
        results = []

    if any(item["question"] == question for item in results):
        print("This question is already saved.")
        print("Existing results were not overwritten.")
        return

    result = run_pipeline(question)
    results.append(result)

    OUTPUT_FILE.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\nQUESTION:")
    print(result["question"])

    print("\nANSWER:")
    print(result["answer"])

    print("\nCITATIONS:")
    print(result["citations"])

    print("\nRETRIEVAL TIME:", result["retrieval_latency_seconds"])
    print("GENERATION TIME:", result["latency_seconds"])
    print("TOTAL TIME:", result["total_latency_seconds"])
    print("FINISH REASON:", result["finish_reason"])
    print("GENERATED TOKENS:", result["generated_tokens"])

    print("\nSaved to:", OUTPUT_FILE)
    print("Total saved questions:", len(results))


if __name__ == "__main__":
    main()
