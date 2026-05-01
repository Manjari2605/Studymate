from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.vector_store import search
from backend.services.llm_service import answer_question, generate_quiz, explain_answer
from backend.services.conversation import (
    store_conversation, 
    get_conversation_context, 
    is_followup_question,
    clear_conversation
)

router = APIRouter(prefix="/chat", tags=["chat"])


class AskRequest(BaseModel):
    question: str
    session_id: str = "default"  # Session ID for conversation history


class QuizRequest(BaseModel):
    topic: str
    num_questions: int = 3


class ExplainRequest(BaseModel):
    question: str
    answer: str


class ClearSessionRequest(BaseModel):
    session_id: str = "default"


@router.post("/ask")
def ask_ai(req: AskRequest):
    """Answer a student's question using RAG. Supports follow-up questions."""
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # Check if this is a follow-up question
    is_followup = is_followup_question(req.question)
    previous_context = None
    
    if is_followup:
        previous_context = get_conversation_context(req.session_id)
        
        # If we have previous context, use those chunks for follow-up
        if previous_context:
            chunks = previous_context["chunks"]
            answer = answer_question(req.question, chunks, previous_context)
        else:
            # Fallback if no previous context
            chunks = search(req.question, top_k=5)
            if not chunks:
                return {"answer": "I couldn't find any relevant content in your notes. Please upload some notes first!"}
            answer = answer_question(req.question, chunks)
    else:
        # Initial question: search for new context
        chunks = search(req.question, top_k=5)

        if not chunks:
            return {"answer": "I couldn't find any relevant content in your notes. Please upload some notes first!"}

        answer = answer_question(req.question, chunks)
    
    # Store this Q&A for potential follow-ups
    store_conversation(req.session_id, req.question, answer, chunks)
    
    return {
        "answer": answer, 
        "sources_used": len(chunks),
        "is_followup": is_followup
    }


@router.post("/clear-session")
def clear_session(req: ClearSessionRequest):
    """Clear conversation history for a session."""
    clear_conversation(req.session_id)
    return {"message": f"Session {req.session_id} cleared."}



@router.post("/quiz")
def create_quiz(req: QuizRequest):
    """Generate a quiz from uploaded notes on a given topic."""
    if not req.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty.")

    chunks = search(req.topic, top_k=6)

    if not chunks:
        return {"quiz": [], "message": "No relevant notes found for this topic."}

    quiz = generate_quiz(req.topic, chunks, req.num_questions)
    return {"quiz": quiz, "topic": req.topic}


@router.post("/explain")
def explain(req: ExplainRequest):
    """Explain why an answer is correct."""
    chunks = search(req.question, top_k=4)
    explanation = explain_answer(req.question, req.answer, chunks)
    return {"explanation": explanation}
