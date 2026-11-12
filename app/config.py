import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL"
)

if not GROQ_API_KEY:
    raise ValueError("Groq API key missing in .env")


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
VECTOR_DIR = BASE_DIR / "vectorstore"

DATA_DIR.mkdir(exist_ok=True)
VECTOR_DIR.mkdir(exist_ok=True)

# Embedding model
EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

# RAG settings
TOP_K = 5

# Starting threshold; validate against actual PDFs
SIMILARITY_THRESHOLD = 0.18
