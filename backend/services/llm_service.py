import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
MODEL = "meta-llama/Llama-3.1-8B-Instruct"

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)


def _call_llm(system: str, user: str, max_tokens: int = 800, temperature: float = 0.4):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()


def answer_question(question: str, context_chunks: list[str], previous_context=None):

    q = question.lower().strip()

    base_context = "\n\n".join(context_chunks[:3])
    advanced_context = "\n\n".join(context_chunks[:5])

    definition_query = q.startswith(
        ("what is", "what are", "define", "meaning of", "what does")
    )

    followup_phrases = [
        "explain more",
        "tell me more",
        "elaborate",
        "more details",
        "more information",
        "expand on",
        "clarify",
        "can you explain more",
        "explain in more detail"
    ]

    followup_expand_query = any(p in q for p in followup_phrases)

    advanced_query = any(
        p in q for p in [
            "in detail",
            "advanced",
            "deep dive",
            "in depth",
            "step by step",
            "thoroughly",
            "comprehensive"
        ]
    )

    explain_query = q.startswith(
        ("explain", "describe", "tell me about", "how does")
    )


    if definition_query:

        system = """
You are StudyMate.

Give a simple beginner-friendly definition.

Rules:
Answer in 2 to 4 short sentences.
Use simple language.
Give one small example if useful.

No markdown.
No bullets.
No stars.
No numbering.
Return clean paragraphs only.
"""

        user = f"""
Reference Notes:
{base_context}

Question:
{question}
"""

        return _call_llm(
            system,
            user,
            max_tokens=150
        )


    elif followup_expand_query:

        if previous_context:

            system = """
You are StudyMate.

Expand the previous answer with more depth.

Use short clean paragraphs.
Explain naturally step by step.
Include one simple example.

Do not use headings.
Do not use markdown.
Do not use bullets.
Do not use numbering.

Finish the explanation completely.
Do not stop midway.
"""

            user = f"""
Previous Answer:
{previous_context['answer']}

Expand this answer.
"""

        else:

            system = """
You are StudyMate.

Give a detailed teacher-style explanation.

Use clean paragraphs.
Include one simple example.

No headings.
No markdown.
No bullets.
No numbering.

Finish the explanation fully.
"""

            user = f"""
Reference Notes:
{base_context}

Question:
{question}
"""

        return _call_llm(
            system,
            user,
            max_tokens=700
        )


    elif explain_query and advanced_query:

        system = """
You are StudyMate.

Give an advanced but clear explanation covering:
what it is,
problem it solves,
how it works,
main components,
real-world applications,
one practical example.

Use flowing paragraphs only.

No section headings.
No markdown.
No stars.
No bullets.
No numbering.

Finish the explanation completely.
Do not stop midway.
"""

        user = f"""
Reference Notes:
{advanced_context}

Question:
{question}
"""

        return _call_llm(
            system,
            user,
            max_tokens=1000
        )


    elif explain_query:

        system = """
You are StudyMate.

Give a medium-level explanation like a teacher.

Explain clearly.
Use clean short paragraphs.
Include one small example.

No headings.
No markdown.
No stars.
No bullets.
No numbering.

Finish the explanation fully.
"""

        user = f"""
Reference Notes:
{base_context}

Question:
{question}
"""

        return _call_llm(
            system,
            user,
            max_tokens=550
        )


    else:

        system = """
You are StudyMate.

Answer naturally like a teacher.
Be concise but complete.
Use provided notes only.

No markdown.
No stars.

Return clean readable paragraphs.
"""

        user = f"""
Reference Notes:
{base_context}

Question:
{question}
"""

        return _call_llm(
            system,
            user,
            max_tokens=350
        )


def generate_quiz(
    topic: str,
    context_chunks: list[str],
    num_questions: int = 3
) -> list[dict]:

    context = "\n\n".join(context_chunks)

    system = """
You are StudyMate quiz generator.

Return ONLY a valid JSON array.
No markdown.
No extra text.
"""

    user = f"""
Generate exactly {num_questions} multiple-choice questions about "{topic}"

Reference Notes:
{context}

Rules:
Test understanding, not memorization.
Exactly 4 options per question.
One correct answer only.

Format:
[
 {{
   "question":"...",
   "options":["A) ...","B) ...","C) ...","D) ..."],
   "answer":"A"
 }}
]

Return JSON only.
"""

    raw = _call_llm(
        system,
        user,
        max_tokens=1500,
        temperature=0.2
    )

    try:
        start = raw.find("[")
        end = raw.rfind("]") + 1
        return json.loads(raw[start:end])

    except Exception:
        return [
            {
                "question":"Could not generate quiz. Try again.",
                "options":[],
                "answer":""
            }
        ]


def explain_answer(
    question: str,
    correct_answer: str,
    context_chunks: list[str]
) -> str:

    context = "\n\n".join(context_chunks)

    system = """
You are StudyMate expert tutor.

Explain why the correct answer is right,
why other options may be wrong,
and give one memory tip.

Use simple clean paragraphs.
No bullets.
No markdown.

Keep it concise in 3 to 5 sentences.
"""

    user = f"""
Reference Notes:
{context}

Question:
{question}

Correct Answer:
{correct_answer}

Explain the answer.
"""

    return _call_llm(
        system,
        user,
        max_tokens=500
    )