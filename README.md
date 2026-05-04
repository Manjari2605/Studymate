# 📚 StudyMate AI

An AI-powered smart study assistant that allows students to upload notes, ask questions, and generate quizzes using Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

- 📄 Upload study materials (PDF, DOCX, TXT)
- 🤖 Ask questions from your notes
- 🧠 Context-aware AI answers (RAG-based)
- 📝 Automatic quiz generation
- 💬 Conversational learning assistant

---

## 📁 Project Structure

studymate/
├── main.py
├── requirements.txt
├── .env
│
├── backend/
│   ├── models/
│   │   └── database.py
│   ├── routers/
│   │   ├── notes.py
│   │   └── chat.py
│   ├── services/
│   │   ├── vector_store.py
│   │   └── llm_service.py
│   └── utils/
│       └── text_extractor.py
│
├── frontend/
│   ├── styles/
│   │   └── main.css
│   └── pages/
│       ├── index.html
│       ├── ask.html
│       └── quiz.html
│
└── data/
    ├── uploads/
    ├── index/
    └── studymate.db

---

## ⚙️ Setup Instructions

### 1. Clone the repository
git clone <your-repo-url>
cd studymate

### 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Add Hugging Face Token
Create/Edit `.env` file:

HUGGINGFACE_TOKEN=your_token_here

Get token from:
https://huggingface.co/settings/tokens

### 5. Run the application
uvicorn main:app --reload

### 6. Open in browser
http://localhost:8000

---

## 🌐 Pages

| Page | URL | Description |
|------|-----|------------|
| Upload Notes | / | Upload study materials |
| Ask AI | /ask | Ask questions from notes |
| Quiz | /quizzes | Generate quizzes |

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|------------|
| POST | /api/notes/upload | Upload a note |
| GET | /api/notes/ | Get all notes |
| DELETE | /api/notes/{id} | Delete note |
| POST | /api/chat/ask | Ask question |
| POST | /api/chat/quiz | Generate quiz |
| POST | /api/chat/explain | Explain answer |

---

## 🧠 Tech Stack

Backend:
- Python
- FastAPI
- Uvicorn

AI / ML:
- Mistral-7B-Instruct (via Hugging Face)
- sentence-transformers (all-MiniLM-L6-v2)
- Retrieval-Augmented Generation (RAG)

Vector Search:
- FAISS (faiss-cpu)

Database:
- SQLite
- SQLAlchemy

Frontend:
- HTML
- CSS
- JavaScript

Tools & Deployment:
- Git & GitHub
- Render
- dotenv (.env for secrets)

---

## 🧩 How It Works

1. Upload notes
2. Text is extracted and chunked
3. Converted into embeddings
4. Stored in FAISS
5. User asks a question
6. Relevant chunks retrieved
7. Sent to LLM → Answer generated
