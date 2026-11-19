import json
import os
from pathlib import Path

from config import LLM_MODEL, LLM_BASE_URL
from generate import generate_answer

if LLM_MODEL != "gpt-5.6-luna":
    raise SystemExit("Set LLM_MODEL=gpt-5.6-luna first")

if not LLM_BASE_URL.startswith("https://"):
    raise SystemExit("Cloud URL is not configured")

if os.getenv("TOKEN_LIMIT_PARAM") != "max_completion_tokens":
    raise SystemExit("Set TOKEN_LIMIT_PARAM=max_completion_tokens first")


def load(filename):
    return json.loads(Path(filename).read_text(encoding="utf-8"))


def normalize(value):
    return " ".join(str(value).casefold().split())


local = load("pipeline_outputs_local.json")
original = load("pipeline_outputs.json")

destination = Path("pipeline_outputs_cloud.json")
cloud = load(destination) if destination.exists() else []
completed = {str(row["id"]) for row in cloud}

for row in local:
    qid = str(row["id"])

    if qid in completed:
        print(f"Q{qid}: already saved")
        continue

    matches = [
        item for item in original
        if normalize(item["question"]) == normalize(row["question"])
    ]

    if not matches:
        raise RuntimeError(f"Missing original chunks: Q{qid}")

    rated = [item for item in matches if item.get("rating_note")]
    source = (rated or matches)[-1]
    chunks = source["retrieved_chunks"]

    if [chunk["text"] for chunk in chunks] != row["retrieved_context"]:
        raise RuntimeError(f"Retrieved context mismatch: Q{qid}")

    print(f"Q{qid}: generating cloud answer...", flush=True)

    result = generate_answer(row["question"], chunks)

    cloud.append({
        **result,
        "id": qid,
        "expected_answer": row["expected_answer"],
        "actual_answer": result["answer"],
        "retrieved_context": row["retrieved_context"],
        "generation_time_ms": round(result["latency_seconds"] * 1000, 2),
        "passed": None,
        "rating_note": "",
    })

    temporary = destination.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(cloud, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temporary.replace(destination)

    completed.add(qid)
    print(f"Q{qid}: saved successfully", flush=True)

print(f"Completed: {len(cloud)} cloud answers")
