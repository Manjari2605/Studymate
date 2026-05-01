# StudyMate AI 📚

A smart study assistant that lets students upload notes and get AI-powered answers and quizzes — built with FastAPI, FAISS, RAG, and Mistral-7B via Hugging Face.

---

## Project Structure

```
studymate/
├── main.py                          # FastAPI app entry point
├── requirements.txt
├── .env                             # Your HuggingFace token goes here
│
├── backend/
│   ├── models/
│   │   └── database.py             # SQLite models (Note, Chunk, Quiz)
│   ├── routers/
│   │   ├── notes.py                # Upload, list, delete notes
│   │   └── chat.py                 # Ask AI, generate quiz, explain
│   ├── services/
│   │   ├── vector_store.py         # FAISS indexing & search
│   │   └── llm_service.py          # Mistral-7B via HuggingFace API
│   └── utils/
│       └── text_extractor.py       # PDF / DOCX / TXT text extraction + chunking
│
├── frontend/
│   ├── styles/
│   │   └── main.css                # Shared styles
│   └── pages/
│       ├── index.html              # Upload Notes page
│       ├── ask.html                # Ask AI chat page
│       └── quiz.html               # Quiz generation page
│
└── data/                           # Auto-created at runtime
    ├── uploads/                    # Uploaded files stored here
    ├── index/                      # FAISS index stored here
    └── studymate.db                # SQLite database
```

---

## Setup

### 1. Clone / open in VS Code
Open the `studymate/` folder in VS Code.

### 2. Create a virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your HuggingFace token
Edit `.env`:
```
HUGGINGFACE_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxx
```
Get your token at: https://huggingface.co/settings/tokens
(Read access is enough)

### 5. Run the app
```bash
uvicorn main:app --reload
```

### 6. Open in browser
```
http://localhost:8000
```

---

## Pages

| Page | URL | What it does |
|---|---|---|
| Upload Notes | `/` | Upload PDF, TXT, DOCX files |
| Ask AI | `/ask` | Chat with AI about your notes |
| Quizzes | `/quizzes` | Generate MCQ quizzes from notes |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/notes/upload` | Upload a note file |
| GET | `/api/notes/` | List all notes |
| DELETE | `/api/notes/{id}` | Delete a note |
| POST | `/api/chat/ask` | Ask a question |
| POST | `/api/chat/quiz` | Generate a quiz |
| POST | `/api/chat/explain` | Explain a quiz answer |

---

## Tech Stack

- **Backend** — Python, FastAPI
- **Vector Search** — FAISS (faiss-cpu)
- **Embeddings** — sentence-transformers (all-MiniLM-L6-v2) — runs locally, free
- **LLM** — Mistral-7B-Instruct via HuggingFace Inference API — free tier
- **Database** — SQLite via SQLAlchemy
- **Frontend** — Vanilla HTML, CSS, JS (no framework needed)
