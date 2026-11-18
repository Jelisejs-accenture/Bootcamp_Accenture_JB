import json

from config import BASE_DIR
from pipeline import run_pipeline, OUTPUT_FILE


questions = json.loads(
    (BASE_DIR / "test_questions.json").read_text(encoding="utf-8")
)

results = (
    json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
    if OUTPUT_FILE.exists()
    else []
)

for question in questions:
    question_id = question["id"]
    question_text = question["question"]

    if any(r.get("question") == question_text for r in results):
        print(f"Question {question_id}: already saved, skipping.")
        continue

    print(
        f"\nRunning question {question_id}/{len(questions)} "
        f"({question['difficulty']})",
        flush=True,
    )

    try:
        result = run_pipeline(question_text)
    except Exception as error:
        print(f"Error on question {question_id}: {error}")
        break

    result["question_id"] = question_id
    result["difficulty"] = question["difficulty"]

    results.append(result)

    temp_file = OUTPUT_FILE.with_suffix(".tmp")
    temp_file.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    temp_file.replace(OUTPUT_FILE)

    print("Answer:", result["answer"])
    print("Citations:", result["citations"])
    print("Time:", result["total_latency_seconds"], "seconds")
    print("Saved successfully.", flush=True)

print("\nEvaluation run finished.")
print("Total saved responses:", len(results))