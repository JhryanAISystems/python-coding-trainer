from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Solve
from app.schemas import ExerciseDetail, ExerciseListResponse, ExerciseSummary, HintResponse
from app.services import exercise_service

router = APIRouter(prefix="/api/exercises", tags=["exercises"])


def _solve_for(db: Session, exercise_id: str) -> Solve | None:
    return db.get(Solve, exercise_id)


@router.get("", response_model=ExerciseListResponse)
def list_exercises(
    topic: str | None = None,
    difficulty: str | None = None,
    db: Session = Depends(get_db),
):
    exercises = exercise_service.list_exercises()
    if topic:
        exercises = [e for e in exercises if e.topic == topic]
    if difficulty:
        exercises = [e for e in exercises if e.difficulty == difficulty]

    solves = {s.exercise_id: s for s in db.scalars(select(Solve))}
    summaries = [
        ExerciseSummary(
            id=e.id,
            title=e.title,
            topic=e.topic,
            difficulty=e.difficulty,
            order=e.order,
            solved=bool(solves.get(e.id) and solves[e.id].solved),
            times_attempted=solves[e.id].times_attempted if e.id in solves else 0,
        )
        for e in exercises
    ]
    return ExerciseListResponse(exercises=summaries, topics=exercise_service.list_topics())


@router.get("/{exercise_id}", response_model=ExerciseDetail)
def get_exercise(exercise_id: str, db: Session = Depends(get_db)):
    try:
        ex = exercise_service.get_exercise(exercise_id)
    except exercise_service.ExerciseNotFoundError:
        raise HTTPException(status_code=404, detail=f"Exercise '{exercise_id}' not found")

    solve = _solve_for(db, exercise_id)
    return ExerciseDetail(
        id=ex.id,
        title=ex.title,
        topic=ex.topic,
        difficulty=ex.difficulty,
        description=ex.description,
        starter_code=ex.starter_code,
        function_name=ex.function_name,
        hint_count=len(ex.hints),
        solved=bool(solve and solve.solved),
        times_attempted=solve.times_attempted if solve else 0,
    )


@router.get("/{exercise_id}/hints/{hint_index}", response_model=HintResponse)
def get_hint(exercise_id: str, hint_index: int, db: Session = Depends(get_db)):
    try:
        ex = exercise_service.get_exercise(exercise_id)
    except exercise_service.ExerciseNotFoundError:
        raise HTTPException(status_code=404, detail=f"Exercise '{exercise_id}' not found")

    if hint_index < 0 or hint_index >= len(ex.hints):
        raise HTTPException(status_code=404, detail="No hint at that index")

    solve = _solve_for(db, exercise_id)
    if solve is None:
        solve = Solve(exercise_id=exercise_id, solved=False, times_attempted=0, times_passed=0, hints_used=0)
        db.add(solve)
    solve.hints_used = max(solve.hints_used, hint_index + 1)
    db.commit()

    return HintResponse(
        exercise_id=exercise_id,
        hint_index=hint_index,
        hint=ex.hints[hint_index],
        hints_remaining=len(ex.hints) - hint_index - 1,
    )
