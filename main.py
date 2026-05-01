from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.models.database import init_db
from backend.routers import notes, chat
import os

app = FastAPI(title="StudyMate AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    os.makedirs("data/uploads", exist_ok=True)
    os.makedirs("data/index", exist_ok=True)
    init_db()

app.include_router(notes.router, prefix="/api")
app.include_router(chat.router,  prefix="/api")

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_index():
    return FileResponse("frontend/pages/index.html")

@app.get("/ask")
def serve_ask():
    return FileResponse("frontend/pages/ask.html")

@app.get("/quizzes")
def serve_quiz():
    return FileResponse("frontend/pages/quiz.html")

@app.get("/health")
def health():
    return {"status": "ok", "app": "StudyMate AI"}
