import asyncio
import sys
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from services import engine
from services.ats_analyzer import analyze_ats
from services.fluency import FluencyAnalyzer
from services.parser import ResumeParser


app = FastAPI(title="Career Match AI & Interview IQ API", version="1.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SpeechEvalRequest(BaseModel):
    transcript: str
    duration_seconds: float


class InterviewQuestionRequest(BaseModel):
    role: str = "Backend Developer"
    category: str = "Technical"
    difficulty: str = "Intermediate"


class InterviewChatRequest(BaseModel):
    message: str
    context: str | None = None
    role: str | None = None


@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Career Match AI & Interview IQ Backend is running!",
    }


@app.get("/api/health")
async def health():
    return {"status": "online", "ai": engine.configuration_status()}


def _read_resume(contents, filename):
    try:
        return ResumeParser.parse(contents, filename or "")
    except (ValueError, KeyError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/analyze-resume")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
):
    """Run the existing local ATS and evidence analysis."""
    contents = await file.read()
    resume_text = _read_resume(contents, file.filename)
    try:
        result = await asyncio.to_thread(
            analyze_ats, resume_text, job_description
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail="Resume analysis failed.") from error
    return {"status": "success", "data": result}


@app.post("/api/ai/resume-analysis")
async def ai_resume_analysis(
    file: UploadFile = File(...),
    job_description: str = Form(...),
):
    """Return a structured Gemini analysis, falling back to Ollama if needed."""
    contents = await file.read()
    resume_text = _read_resume(contents, file.filename)
    try:
        result = await asyncio.to_thread(
            engine.analyze_resume, resume_text, job_description
        )
        return result
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except engine.AIEngineError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error


@app.post("/api/evaluate-speech")
async def evaluate_speech(payload: SpeechEvalRequest):
    if payload.duration_seconds <= 0:
        raise HTTPException(status_code=400, detail="Duration must be greater than zero.")
    try:
        results = FluencyAnalyzer.analyze_transcript(
            payload.transcript, payload.duration_seconds
        )
        return {"status": "success", "data": results}
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/generate-question")
async def generate_question(payload: InterviewQuestionRequest):
    try:
        result = await asyncio.to_thread(
            engine.generate_questions,
            payload.role,
            payload.category,
            payload.difficulty,
        )
        return {
            "status": "success",
            "provider": result["provider"],
            "questions": result["answer"],
        }
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except engine.AIEngineError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error


@app.post("/api/ai/chat")
async def interview_chat(payload: InterviewChatRequest):
    try:
        result = await asyncio.to_thread(
            engine.chat, payload.message, payload.context, payload.role
        )
        return {"status": "success", **result}
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except engine.AIEngineError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
