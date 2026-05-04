# 📚 StudyMate AI – Smart Learning Assistant

## Overview

StudyMate AI is an AI-powered educational assistant that transforms static study materials into an interactive learning experience. It allows users to upload notes, ask questions, generate quizzes, and receive intelligent, context-aware explanations using advanced AI and semantic retrieval techniques.

---

## Features

### Document Upload & Processing
- Supports PDF, DOCX, and TXT files  
- Extracts and processes text automatically  

### AI Question Answering
- Ask questions from uploaded notes  
- Get contextual and accurate answers  

### Semantic Retrieval
- Uses vector embeddings for intelligent search  
- Retrieves relevant content based on meaning  

### Automatic Quiz Generation
- Generates quizzes from study materials  
- Helps in revision and self-assessment  

### Conversational Assistant
- Supports follow-up questions  
- Acts like a virtual tutor  

---

## Tech Stack

### Backend
- Python  
- FastAPI  

### AI / ML
- Llama 3.1 8B Instruct  
- Hugging Face Transformers  
- Sentence Transformers (all-MiniLM-L6-v2)  

### Retrieval
- FAISS (Vector Database)  

### Database
- SQLite  

### Document Processing
- PyPDF  
- python-docx  

### Deployment
- Render (Cloud Platform)  

---

## Project Structure

```
studymate-ai/
│
├── backend/
│   ├── models/
│   ├── routers/
│   ├── services/
│   ├── utils/
│
├── data/
│   ├── index/
│   ├── uploads/
│   └── studymate.db
│
├── frontend/
│   ├── pages/
│   └── styles/
│
├── main.py
├── requirements.txt
├── .env
```

---

## Installation & Setup

### Clone the Repository
```
git clone https://github.com/Manjari2605/Studymate.git
cd studymate-ai
```

### Create Virtual Environment
```
python -m venv myenv

# Linux/Mac
source myenv/bin/activate  

# Windows
myenv\Scripts\activate
```

### Install Dependencies
```
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file and add:
```
HUGGINGFACE_API_KEY=your_api_key_here
```

---

## Run the Application

```
uvicorn main:app --reload
```

Open in browser:
```
http://127.0.0.1:8000
```

---

## Deployment

This project is deployed using Render.

### Steps:
1. Create a new Web Service on Render  
2. Connect GitHub repository  
3. Set build command:
```
pip install -r requirements.txt
```
4. Set start command:
```
uvicorn main:app --host 0.0.0.0 --port 10000
```
5. Add environment variables (.env values)  

---

## Use Cases

- Exam preparation  
- Concept understanding  
- Automated revision  
- Self-assessment through quizzes  
- Personalized learning assistant  
