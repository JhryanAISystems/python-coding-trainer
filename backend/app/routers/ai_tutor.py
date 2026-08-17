import logging

from fastapi import APIRouter, HTTPException

from app.config import get_settings
from app.schemas import (
    AIStatusResponse,
    CodeReviewRequest,
    CodeReviewResponse,
    GenerateExerciseRequest,
    GeneratedExercise,
)
from app.services import ai_service, exercise_service

logger = logging.getLogger("app.ai_tutor")
router = APIRouter(prefix="/api/ai", tags=["ai-tutor"])
settings = get_settings()


@router.get("/status", response_model=AIStatusResponse)
def ai_status():
    if settings.anthropic_api_key:
        return AIStatusResponse(enabled=True, provider="anthropic")
    if settings.openai_api_key:
        return AIStatusResponse(enabled=True, provider="openai")
    return AIStatusResponse(enabled=False, provider=None)


def _require_ai() -> None:
    if not settings.ai_enabled:
        raise HTTPException(
            status_code=503,
            detail="AI tutor mode is not configured. Set ANTHROPIC_API_KEY to enable it.",
        )


@router.post("/generate-exercise", response_model=GeneratedExercise)
def generate_exercise(payload: GenerateExerciseRequest):
    _require_ai()
    try:
        return ai_service.generate_exercise(payload)
    except Exception:
        logger.exception("AI exercise generation failed")
        raise HTTPException(status_code=502, detail="The AI tutor is unavailable right now.")


@router.post("/review", response_model=CodeReviewResponse)
def review_code(payload: CodeReviewRequest):
    _require_ai()
    try:
        ex = exercise_service.get_exercise(payload.exercise_id)
    except exercise_service.ExerciseNotFoundError:
        raise HTTPException(status_code=404, detail=f"Exercise '{payload.exercise_id}' not found")
    try:
        review = ai_service.review_code(payload, ex.title, ex.description)
        return CodeReviewResponse(review=review)
    except Exception:
        logger.exception("AI code review failed")
        raise HTTPException(status_code=502, detail="The AI tutor is unavailable right now.")
