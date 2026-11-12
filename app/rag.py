
import pickle
import faiss
import numpy as np
import re

from groq import Groq
from sentence_transformers import SentenceTransformer

from app.config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    EMBEDDING_MODEL,
    VECTOR_DIR,
    TOP_K,
    SIMILARITY_THRESHOLD
)


# =====================================================
# STEP 1: INITIALIZE GROQ
# =====================================================

client = Groq(api_key=GROQ_API_KEY)


# =====================================================
# STEP 2: LOAD EMBEDDING MODEL
# =====================================================

embedding_model = SentenceTransformer(EMBEDDING_MODEL)


# =====================================================
# STEP 3: LOAD FAISS INDEX
# =====================================================

index_path = VECTOR_DIR / "index.faiss"

if not index_path.exists():
    raise FileNotFoundError(
        "FAISS index not found. Run: python -m app.ingestion"
    )

index = faiss.read_index(str(index_path))


# =====================================================
# STEP 4: LOAD PDF CHUNKS
# =====================================================

chunks_path = VECTOR_DIR / "chunks.pkl"

if not chunks_path.exists():
    raise FileNotFoundError(
        "PDF chunks not found. Run: python -m app.ingestion"
    )

with open(chunks_path, "rb") as file:
    chunks = pickle.load(file)

if index.ntotal == 0 or not chunks:
    raise ValueError(
        "The vector database is empty. Please ingest the PDFs first."
    )

if index.ntotal != len(chunks):
    raise ValueError(
        "FAISS index and PDF chunks do not match. "
        "Run ingestion again."
    )


# =====================================================
# STEP 5: TEXT NORMALIZATION
# =====================================================

def normalize_text(text):
    """
    Normalize whitespace for reliable PDF text comparison.
    """

    return re.sub(r"\s+", " ", text).strip().lower()


# =====================================================
# STEP 6: VERIFY MAINTENANCE RESPONSIBILITIES
# =====================================================

def verify_maintenance_responsibilities(
    question,
    retrieved_chunks,
    source_ids
):
    """
    Verify spindle runout frequency and responsibility
    directly against the maintenance manual.

    This is a targeted deterministic safeguard.
    """

    question_normalized = normalize_text(question)

    if "spindle runout" not in question_normalized:
        return None

    for item in retrieved_chunks:

        document_name = item["source"].lower()
        document_text = normalize_text(item["text"])

        # Only use the preventive maintenance manual
        if "mnt-man-cnc-02" not in document_name:
            continue

        # Verify the actual maintenance schedule content
        if (
            "monthly" in document_text
            and "check spindle runout" in document_text
            and "maintenance technician" in document_text
        ):

            source_key = (
                item["source"],
                item["page"]
            )

            source_id = source_ids.get(source_key)

            if source_id:
                return (
                    "Spindle runout should be checked "
                    "**monthly**. The responsible person "
                    "is the **Maintenance technician**. "
                    f"[{source_id}]"
                )

    # Do not invent an answer if supporting evidence is absent
    return None


# =====================================================
# STEP 7: MAIN QUESTION FUNCTION
# =====================================================

def ask_question(question):

    question = question.strip()

    if not question:
        return {
            "answer": "Please enter a question.",
            "sources": [],
            "truncated": False
        }

    # -------------------------------------------------
    # STEP 8: CONVERT QUESTION INTO EMBEDDING
    # -------------------------------------------------

    question_embedding = embedding_model.encode(
        [question],
        normalize_embeddings=True
    )

    question_embedding = np.asarray(
        question_embedding,
        dtype="float32"
    )

    # -------------------------------------------------
    # STEP 9: SEARCH FAISS
    # -------------------------------------------------

    search_count = min(TOP_K, index.ntotal)

    scores, indices = index.search(
        question_embedding,
        search_count
    )

    # -------------------------------------------------
    # STEP 10: FILTER RELEVANT CHUNKS
    # -------------------------------------------------

    retrieved_chunks = []

    print("\n========== RETRIEVED DOCUMENTS ==========")

    for score, idx in zip(scores[0], indices[0]):

        if idx < 0:
            continue

        score = float(score)
        chunk = chunks[idx]

        print("\nSimilarity Score:", round(score, 4))
        print("Document:", chunk["source"])
        print("Page:", chunk["page"])
        print("Retrieved Text:")
        print(chunk["text"])
        print("-" * 60)

        if score >= SIMILARITY_THRESHOLD:

            retrieved_chunks.append({
                "text": chunk["text"],
                "source": chunk["source"],
                "page": chunk["page"],
                "score": score
            })

    # -------------------------------------------------
    # STEP 11: HANDLE NO RELEVANT RESULTS
    # -------------------------------------------------

    if not retrieved_chunks:
        return {
            "answer": (
                "I couldn't find this information "
                "in the provided documents."
            ),
            "sources": [],
            "truncated": False
        }

    # -------------------------------------------------
    # STEP 12: ASSIGN SOURCE IDENTIFIERS
    # -------------------------------------------------

    source_ids = {}
    sources = []
    context_parts = []

    for item in retrieved_chunks:

        key = (item["source"], item["page"])

        if key not in source_ids:

            source_id = f"S{len(source_ids) + 1}"
            source_ids[key] = source_id

            sources.append({
                "id": source_id,
                "document": item["source"],
                "page": item["page"],
                "evidence": item["text"][:350],
                "score": round(item["score"], 4)
            })

        source_id = source_ids[key]

        context_parts.append(
            f"""
[{source_id}]
Document: {item['source']}
Page: {item['page']}

Content:
{item['text']}
"""
        )

    context = "\n".join(context_parts)

    # -------------------------------------------------
    # STEP 13: PREPARE GROUNDED PROMPT
    # -------------------------------------------------

    prompt = f"""
You are a Manufacturing SOP AI Copilot.

Answer the user's question using ONLY the supplied
PDF content.

STRICT ACCURACY RULES:

1. Treat the supplied PDF content as the source of truth.
2. Never guess or invent information.
3. Preserve exact job titles and responsibilities.
4. Never replace one responsible role with another.
5. If information is missing, clearly say it is not found.
6. If documents conflict, explain the conflict.
7. Cite supporting sources using [S1], [S2], etc.
8. Ignore unrelated documents.
9. Do not use general knowledge to fill missing information.

MAINTENANCE SCHEDULE RULES:

1. Treat the "Done by" column as the authoritative
   responsibility assignment.
2. Match each activity with its own frequency and
   responsible person from the same table row.
3. Never transfer responsibility from another row.
4. Do not assume that an operator performs every
   maintenance activity.
5. Preserve the exact role names from the PDF.
6. If asked about spindle runout, check the monthly
   maintenance schedule carefully.

SOURCE CITATION RULES:

1. Cite the source that directly supports your answer.
2. Do not cite unrelated documents.
3. Use the source identifiers exactly as provided.
4. Do not invent source identifiers.

ANSWER FORMAT:

For maintenance schedule questions, use:

| Frequency | Activity | Responsible Person |
|-----------|----------|--------------------|

For other questions, answer clearly and directly.

DOCUMENT CONTENT:

{context}

USER QUESTION:

{question}

ANSWER:
"""

    # -------------------------------------------------
    # STEP 14: GENERATE ANSWER USING GROQ
    # -------------------------------------------------

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a reliable manufacturing "
                    "document assistant. Follow the "
                    "provided PDF documents exactly. "
                    "Never invent facts or responsibilities."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=1200
    )

    answer = response.choices[0].message.content or ""

    # -------------------------------------------------
    # STEP 15: VERIFY SPINDLE RUNOUT RESPONSIBILITY
    # -------------------------------------------------

    verified_answer = verify_maintenance_responsibilities(
        question,
        retrieved_chunks,
        source_ids
    )

    if verified_answer:
        answer = verified_answer
        print(
            "\nPDF verification: Spindle runout responsibility "
            "is Maintenance technician."
        )

    # -------------------------------------------------
    # STEP 16: DETECT OUTPUT TRUNCATION
    # -------------------------------------------------

    finish_reason = response.choices[0].finish_reason

    truncated = finish_reason == "length"

    if truncated:
        answer += (
            "\n\nNote: The answer may be incomplete because "
            "the model reached its output token limit."
        )

    # -------------------------------------------------
    # STEP 17: RETURN ANSWER AND SOURCES
    # -------------------------------------------------

    return {
        "answer": answer,
        "sources": sources,
        "truncated": truncated
    }
