import sys
import chromadb
from openai import OpenAI

from config import (
    CHROMA_DIR,
    COLLECTION_NAME,
    LLM_BASE_URL,
    LLM_API_KEY,
    EMBEDDING_MODEL,
    TOP_K,
)


def retrieve(question: str, top_k: int = TOP_K):
    embedding_client = OpenAI(
        base_url=LLM_BASE_URL,
        api_key=LLM_API_KEY,
        timeout=600,
    )

    response = embedding_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[question],
    )

    question_embedding = response.data[0].embedding

    db_client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    collection = db_client.get_collection(
        name=COLLECTION_NAME
    )

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    chunks = []

    for chunk_id, text, metadata, distance in zip(
        results["ids"][0],
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({
            "id": chunk_id,
            "text": text,
            "source": metadata["source"],
            "page": metadata["page"],
            "chunk": metadata["chunk"],
            "distance": round(float(distance), 4),
            "score": round(1 - float(distance), 4),
        })

    return chunks


if __name__ == "__main__":
    question = " ".join(sys.argv[1:])

    if not question:
        question = "What are the company's security requirements?"

    print(f"\nQuestion: {question}\n")

    chunks = retrieve(question)

    for index, chunk in enumerate(chunks, start=1):
        print(f"--- Result {index} ---")
        print(f"Source: {chunk['source']}")
        print(f"Page: {chunk['page']}")
        print(f"Similarity score: {chunk['score']}")
        print(f"Text:\n{chunk['text']}\n")