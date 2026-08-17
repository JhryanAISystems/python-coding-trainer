"""Optional AI tutor mode. Only active when ANTHROPIC_API_KEY is set; the
app must work fully without it (bundled exercises are the source of truth).
"""
from __future__ import annotations

import json
import logging

from app.config import get_settings
from app.schemas import CodeReviewRequest, GeneratedExercise, GenerateExerciseRequest

logger = logging.getLogger("app.ai")
settings = get_settings()

MODEL = "claude-opus-5"

EXERCISE_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "description": {"type": "string"},
        "starter_code": {"type": "string"},
        "function_name": {"type": "string"},
    },
    "required": ["title", "description", "starter_code", "function_name"],
    "additionalProperties": False,
}


def _client():
    import anthropic

    return anthropic.Anthropic(api_key=settings.anthropic_api_key)


def generate_exercise(req: GenerateExerciseRequest) -> GeneratedExercise:
    client = _client()
    prompt = (
        f"Write a fresh Python coding exercise on the topic '{req.topic}' at "
        f"{req.difficulty} difficulty. Give it a short title, a 2-4 sentence "
        f"markdown description of the task, a starter_code snippet defining a "
        f"function stub (with a docstring, raising NotImplementedError), and "
        f"function_name matching the stub's function name."
    )
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        output_config={"format": {"type": "json_schema", "schema": EXERCISE_SCHEMA}},
        messages=[{"role": "user", "content": prompt}],
    )
    text = next(b.text for b in response.content if b.type == "text")
    data = json.loads(text)
    return GeneratedExercise(**data)


def review_code(req: CodeReviewRequest, exercise_title: str, exercise_description: str) -> str:
    client = _client()
    prompt = (
        f"A learner is working on this Python exercise:\n\n"
        f"Title: {exercise_title}\nDescription: {exercise_description}\n\n"
        f"Their current code:\n```python\n{req.code}\n```\n\n"
        f"Give a short, encouraging code review (3-6 sentences): point out the "
        f"likely bug or gap, without giving away the full solution."
    )
    response = client.messages.create(
        model=MODEL,
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return next(b.text for b in response.content if b.type == "text")
