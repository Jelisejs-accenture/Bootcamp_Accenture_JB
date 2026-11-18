from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_DIR = BASE_DIR.parent / "capstone" / "day11_capstone" / "documents"
CHROMA_DIR = BASE_DIR / "chroma_db"

LLM_BASE_URL = "http://localhost:11434/v1"
LLM_API_KEY = "ollama"
LLM_MODEL = "qwen3.5:2b-q4_K_M"

EMBEDDING_MODEL = "nomic-embed-text"
COLLECTION_NAME = "company_documents"

CHUNK_SIZE = 900
CHUNK_OVERLAP = 150
TOP_K = 4

TEMPERATURE = 0.2
MAX_OUTPUT_TOKENS = 1024
TOKEN_LIMIT_PARAM = "max_tokens"