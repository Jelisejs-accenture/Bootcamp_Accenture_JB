import json
import re
from pathlib import Path

import chromadb

from config import BASE_DIR, CHROMA_DIR, COLLECTION_NAME
from generate import generate_answer

questions = json.loads(
    (BASE_DIR / "test_questions.json").read_text(encoding="utf-8")
)
question = next(q for q in questions if q["id"] == 13)

db = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = db.get_collection(COLLECTION_NAME)

data = collection.get(
    where={"source": "meeting_notes.pdf"},
    include=["documents", "metadatas"],
)

rows = []

for chunk_id, text, metadata in zip(
    data["ids"], data["documents"], data["metadatas"]
):
    rows.append({
        "id": chunk_id,
        "text": text,
        "source": metadata["source"],
        "page": metadata["page"],
        "chunk": metadata["chunk"],
        "score": None,
    })

by_position = {
    (r["page"], r["chunk"]): r
    for r in rows
}

headings = [
    r for r in rows
    if "action items" in r["text"].lower()
]

if not headings:
    raise RuntimeError("No Action Items sections found.")

selected_ids = set()

for heading in headings:
    for offset in [-1, 0, 1, 2]:
        key = (heading["page"], heading["chunk"] + offset)
        chunk = by_position.get(key)

        if chunk:
            selected_ids.add(chunk["id"])

chunks = sorted(
    [r for r in rows if r["id"] in selected_ids],
    key=lambda r: (r["page"], r["chunk"]),
)

print("Retrieved chunks:", len(chunks))
print("Pages:", sorted(set(r["page"] for r in chunks)))

for chunk in chunks:
    print(
        chunk["source"],
        "page", chunk["page"],
        "chunk", chunk["chunk"]
    )

augmented_question = (
    question["question"]
    + "\nGroup the action items by responsible owner. "
      "Include concrete tasks and relevant business priorities. "
      "Cite the meeting notes with [meeting_notes.pdf, p. X]. "
      "Avoid repetition and unrelated policies."
)

print("\nGenerating improved answer...", flush=True)

result = generate_answer(augmented_question, chunks)

result["evaluation_question"] = question["question"]
result["question_id"] = 13
result["difficulty"] = "hard"
result["retrieval_method"] = "section_keyword_with_neighbor_chunks"

matches = re.findall(
    r"\[([^\[\]]+?\.pdf),\s*(?:p\.|page)\s*(\d+)\]",
    result["answer"],
    flags=re.IGNORECASE,
)

result["citations"] = [
    {"source": source, "page": int(page)}
    for source, page in dict.fromkeys(matches)
]

result["passed"] = None
result["rating_note"] = ""

path = BASE_DIR / "retry_q13_targeted.json"
path.write_text(
    json.dumps(result, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

print("\nFINISH REASON:", result["finish_reason"])
print("TOKENS:", result["generated_tokens"])
print("CITATIONS:", result["citations"])
print("\nANSWER:\n", result["answer"])
print("\nSaved to:", path.name)
