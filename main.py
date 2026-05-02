from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.models.database import init_db
from backend.routers import notes, chat
import os

app = FastAPI(title="StudyMate AI", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ SAFE Startup (prevents crash)
@app.on_event("startup")
def startup():
    try:
        os.makedirs("data", exist_ok=True)
        os.makedirs("data/uploads", exist_ok=True)
        os.makedirs("data/index", exist_ok=True)

        init_db()
        print("✅ Database initialized")

    except Exception as e:
        print("❌ Startup error:", e)


# Routers
app.include_router(notes.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

# ✅ SAFE static mount
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

# ✅ SAFE routes
@app.get("/")
def serve_index():
    path = "frontend/pages/index.html"
    if os.path.exists(path):
        return FileResponse(path)
    return {"message": "StudyMate API running"}

@app.get("/ask")
def serve_ask():
    path = "frontend/pages/ask.html"
    if os.path.exists(path):
        return FileResponse(path)
    return {"message": "Ask page not found"}

@app.get("/quizzes")
def serve_quiz():
    path = "frontend/pages/quiz.html"
    if os.path.exists(path):
        return FileResponse(path)
    return {"message": "Quiz page not found"}

@app.get("/health")
def health():
    return {"status": "ok", "app": "StudyMate AI"}