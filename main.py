
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.rag import ask_question

# Initialize FastAPI
app = FastAPI(
    title="Manufacturing AI Copilot",
    description="AI assistant for manufacturing documents",
    version="1.0.0"
)

# Project paths
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# Serve frontend files
app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)

# Request model
class QuestionRequest(BaseModel):
    question: str

# Home page
@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")

# Ask AI endpoint
@app.post("/ask")
def ask(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Please enter a question."
        )

    try:
        result = ask_question(question)
        return result

    except Exception as error:
        print("Error:", error)
        raise HTTPException(
            status_code=500,
            detail="Unable to process your question."
        )
