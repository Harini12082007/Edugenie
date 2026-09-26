from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


# Create FastAPI application
app = FastAPI(
    title="EduGenie - Gemini Learning Assistant",
    description="AI-powered learning assistant using Google Gemini",
    version="1.0.0"
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# Request model
class TextRequest(BaseModel):
    text: str


# -----------------------------
# HOME PAGE
# -----------------------------

@app.get("/")
async def home():
    return FileResponse("templates/index.html")


# -----------------------------
# VALIDATE INPUT
# -----------------------------

def validate_text(text: str) -> str:
    text = (text or "").strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Please enter some content."
        )

    return text


# -----------------------------
# ASK QUESTION
# -----------------------------

@app.post("/qa")
async def qa(data: TextRequest):

    text = validate_text(data.text)

    try:
        answer = answer_question(text)

        return {
            "answer": answer
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# -----------------------------
# EXPLAIN TOPIC
# -----------------------------

@app.post("/explain")
async def explain(data: TextRequest):

    text = validate_text(data.text)

    try:
        answer = explain_topic(text)

        return {
            "answer": answer
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# -----------------------------
# GENERATE QUIZ
# -----------------------------

@app.post("/quiz")
async def quiz(data: TextRequest):

    text = validate_text(data.text)

    try:
        quiz_data = generate_quiz(text)

        return {
            "quiz": quiz_data
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# -----------------------------
# SUMMARIZE TEXT
# -----------------------------

@app.post("/summarize")
async def summarize(data: TextRequest):

    text = validate_text(data.text)

    try:
        summary = summarize_text(text)

        return {
            "summary": summary
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# -----------------------------
# LEARNING PATH
# -----------------------------

@app.post("/learn/recommendations")
async def learn(data: TextRequest):

    text = validate_text(data.text)

    try:
        recommendations = get_learning_recommendations(text)

        return {
            "recommendations": recommendations
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )