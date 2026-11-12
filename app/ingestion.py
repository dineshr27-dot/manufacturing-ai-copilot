
import os
import pickle
import faiss
import numpy as np

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


DATA_DIR = "data"
VECTOR_DIR = "vectorstore"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

os.makedirs(VECTOR_DIR, exist_ok=True)

embedding_model = SentenceTransformer(MODEL_NAME)


def extract_pdf_pages():
    documents = []

    for filename in os.listdir(DATA_DIR):

        if not filename.lower().endswith(".pdf"):
            continue

        filepath = os.path.join(DATA_DIR, filename)

        reader = PdfReader(filepath)

        for page_number, page in enumerate(reader.pages, start=1):

            text = page.extract_text() or ""

            if text.strip():
                documents.append({
                    "text": text,
                    "source": filename,
                    "page": page_number
                })

    return documents


def split_text(text, chunk_size=800, overlap=150):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_vectorstore():

    pages = extract_pdf_pages()

    if not pages:
        raise ValueError("No readable PDF text found in data/")

    all_chunks = []

    for page in pages:

        chunks = split_text(page["text"])

        for chunk in chunks:

            all_chunks.append({
                "text": chunk,
                "source": page["source"],
                "page": page["page"]
            })

    texts = [item["text"] for item in all_chunks]

    embeddings = embedding_model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True
    )

    embeddings = np.asarray(embeddings, dtype="float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])

    index.add(embeddings)

    faiss.write_index(
        index,
        os.path.join(VECTOR_DIR, "index.faiss")
    )

    with open(
        os.path.join(VECTOR_DIR, "chunks.pkl"),
        "wb"
    ) as file:

        pickle.dump(all_chunks, file)

    print(f"Successfully indexed {len(all_chunks)} chunks")


if __name__ == "__main__":
    create_vectorstore()
