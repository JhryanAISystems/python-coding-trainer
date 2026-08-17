import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.rate_limit import limiter
from app.schemas import SubmitRequest, SubmitResponse
from app.services import exercise_service
from app.services.grading_service import grade_submission

logger = logging.getLogger("app.submissions")
router = APIRouter(prefix="/api/exercises", tags=["submissions"])


@router.post("/{exercise_id}/submit", response_model=SubmitResponse)
@limiter.limit("30/minute")
def submit_solution(
    exercise_id: str,
    payload: SubmitRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        ex = exercise_service.get_exercise(exercise_id)
    except exercise_service.ExerciseNotFoundError:
        raise HTTPException(status_code=404, detail=f"Exercise '{exercise_id}' not found")

    logger.info("grading exercise=%s mode=%s code_len=%d", exercise_id, payload.mode, len(payload.code))
    try:
        return grade_submission(db, ex, payload.code, payload.mode)
    except Exception:
        logger.exception("grading failed for exercise=%s", exercise_id)
        raise HTTPException(status_code=500, detail="Grading failed unexpectedly. Please try again.")
