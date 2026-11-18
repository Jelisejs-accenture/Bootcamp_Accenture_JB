import json
import shutil
from pathlib import Path

questions_path = Path("test_questions.json")
results_path = Path("pipeline_outputs.json")
backup_path = Path("pipeline_outputs_before_review.json")

if not backup_path.exists():
    shutil.copy2(results_path, backup_path)

questions = json.loads(
    questions_path.read_text(encoding="utf-8")
)
results = json.loads(
    results_path.read_text(encoding="utf-8")
)

for q in questions:
    result = next(
        (r for r in results if r.get("question_id") == q["id"]),
        None
    )

    if result is None:
        print(f"Question {q['id']}: missing result")
        continue

    if result.get("passed") is not None:
        print(f"Question {q['id']}: already reviewed")
        continue

    print("\n" + "=" * 60)
    print(f"QUESTION {q['id']} ({q['difficulty']})")
    print(q["question"])

    print("\nEXPECTED ANSWER:")
    print(q["expected_answer"])

    print("\nACTUAL ANSWER:")
    print(result["answer"])

    print("\nCITATIONS:", result.get("citations", []))
    print("FINISH REASON:", result.get("finish_reason"))

    choice = input("\nPassed? [y/n/s to skip]: ").strip().lower()

    if choice not in ("y", "n"):
        continue

    note = input("Reason for your rating: ").strip()

    if not note:
        print("A rating note is required. Skipping.")
        continue

    result["passed"] = choice == "y"
    result["rating_note"] = note

    results_path.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("Review saved.")

print("\nReview session completed.")
print(
    "Reviewed:",
    sum(
        r.get("passed") is not None
        for r in results
        if "question_id" in r
    ),
    "/15"
)
