import chromadb
from openai import OpenAI
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import (
    DOCUMENTS_DIR,
    CHROMA_DIR,
    LLM_BASE_URL,
    LLM_API_KEY,
    EMBEDDING_MODEL,
    COLLECTION_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)


def main():
    pdf_files = sorted(DOCUMENTS_DIR.glob("*.pdf"))

    print("PDF files found:", len(pdf_files))

    if len(pdf_files) != 5:
        raise RuntimeError(
            f"Expected 5 PDF files in {DOCUMENTS_DIR}"
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )

    ids = []
    documents = []
    metadatas = []

    for pdf_file in pdf_files:
        reader = PdfReader(str(pdf_file))
        file_chunks = 0

        for page_number, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").strip()

            if not text:
                continue

            chunks = splitter.split_text(text)

            for chunk_number, chunk in enumerate(chunks):
                ids.append(
                    f"{pdf_file.stem}_p{page_number}_c{chunk_number}"
                )
                documents.append(chunk)
                metadatas.append({
                    "source": pdf_file.name,
                    "page": page_number,
                    "chunk": chunk_number,
                })

            file_chunks += len(chunks)

        print(f"{pdf_file.name}: {file_chunks} chunks", flush=True)

    if not documents:
        raise RuntimeError("No extractable text found in PDFs.")

    print("\nCreating embeddings locally...")

    embedding_client = OpenAI(
        base_url=LLM_BASE_URL,
        api_key=LLM_API_KEY,
        timeout=600,
    )

    db_client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    collection = db_client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    batch_size = 8

    for start in range(0, len(documents), batch_size):
        end = min(start + batch_size, len(documents))

        batch_texts = documents[start:end]

        response = embedding_client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=batch_texts,
        )

        embeddings = [
            item.embedding
            for item in sorted(response.data, key=lambda x: x.index)
        ]

        collection.upsert(
            ids=ids[start:end],
            documents=batch_texts,
            embeddings=embeddings,
            metadatas=metadatas[start:end],
        )

        print(
            f"Saved {end}/{len(documents)} chunks",
            flush=True,
        )

    print("\nIngestion complete!")
    print("Total chunks in ChromaDB:", collection.count())
    print("Database:", CHROMA_DIR)


if __name__ == "__main__":
    main()