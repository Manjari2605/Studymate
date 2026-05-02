from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from openai import OpenAI

router = APIRouter(prefix="/chat", tags=["chat"])

# Load HuggingFace API
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

if not HF_TOKEN:
    raise ValueError("HUGGINGFACE_TOKEN is not set")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)


class AskRequest(BaseModel):
    question: str


@router.post("/ask")
def ask_ai(req: AskRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=[
                {"role": "system", "content": "You are a helpful study assistant."},
                {"role": "user", "content": req.question}
            ],
            max_tokens=300,
        )

        answer = response.choices[0].message.content

        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))