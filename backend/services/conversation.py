"""Manage conversation history and context for follow-up questions."""

from typing import Optional

# In-memory storage: session_id -> list of {question, answer, chunks}
# In production, use Redis or database
conversations = {}


def store_conversation(session_id: str, question: str, answer: str, chunks: list[str]):
    """Store a Q&A pair with its retrieved chunks."""
    if session_id not in conversations:
        conversations[session_id] = []
    
    conversations[session_id].append({
        "question": question,
        "answer": answer,
        "chunks": chunks
    })
    
    # Keep only last 5 exchanges to avoid token overflow
    if len(conversations[session_id]) > 5:
        conversations[session_id].pop(0)


def get_conversation_context(session_id: str) -> Optional[dict]:
    """Get the most recent Q&A context for follow-ups."""
    if session_id not in conversations or not conversations[session_id]:
        return None
    return conversations[session_id][-1]


def clear_conversation(session_id: str):
    """Clear conversation history for a session."""
    if session_id in conversations:
        del conversations[session_id]


def is_followup_question(question: str) -> bool:
    """Detect if a question is likely a follow-up (vague or incomplete)."""
    followup_keywords = [
        "explain more",
        "more details",
        "tell me more",
        "clarify",
        "what do you mean",
        "more clearly",
        "more information",
        "elaborate",
        "give more info",
        "expand",
        "example",
        "how",
        "why",
        "further"
    ]
    
    question_lower = question.lower().strip()
    
    # Check if question contains followup keywords
    for keyword in followup_keywords:
        if keyword in question_lower:
            return True
    
    # Check if question is very short (less than 5 words and no question mark context)
    word_count = len(question_lower.split())
    if word_count <= 5 and not any(word in question_lower for word in ["what is", "who is", "where is", "when is"]):
        return True
    
    return False
