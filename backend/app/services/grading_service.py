"""Orchestrates grading: exercise lookup -> sandbox execution -> persistence."""
from __future__ import annotations

from datetime import datetime, date, timezone
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import Attempt, Solve, StreakDay
from app.sandbox.runner import run_submission
from app.schemas import SubmitResponse, TestCaseResult
from app.services.exercise_service import Exercise

settings = get_settings()


def grade_submission(db: Session, exercise: Exercise, code: str, mode: str) -> SubmitResponse:
    result = run_submission(
        code=code,
        function_name=exercise.function_name,
        test_cases=exercise.test_cases,
        timeout_seconds=settings.sandbox_timeout_seconds,
        memory_mb=settings.sandbox_memory_mb,
    )

    results = [
        TestCaseResult(
            name=r["name"],
            passed=r["passed"],
            input_repr=r["input_repr"],
            expected_repr=r["expected_repr"],
            actual_repr=r.get("actual_repr"),
            error=r.get("error"),
            stdout=r.get("stdout") or None,
        )
        for r in result.results
    ]

    newly_solved = False

    if mode == "submit":
        attempt = Attempt(
            exercise_id=exercise.id,
            code=code,
            mode=mode,
            passed=result.passed,
            total_tests=result.total_tests,
            passed_tests=result.passed_tests,
            results_json=result.results,
            duration_ms=result.duration_ms,
            error=result.error,
        )
        db.add(attempt)

        solve = db.get(Solve, exercise.id)
        if solve is None:
            solve = Solve(exercise_id=exercise.id, solved=False, times_attempted=0, times_passed=0, hints_used=0)
            db.add(solve)
        solve.times_attempted += 1
        if result.passed:
            solve.times_passed += 1
            if not solve.solved:
                solve.solved = True
                solve.first_solved_at = datetime.now(timezone.utc)
                newly_solved = True

        today = date.today()
        day_row = db.get(StreakDay, today)
        if day_row is None:
            day_row = StreakDay(day=today, attempts=0, solves=0)
            db.add(day_row)
        day_row.attempts += 1
        if result.passed:
            day_row.solves += 1

        db.commit()

    return SubmitResponse(
        exercise_id=exercise.id,
        mode=mode,
        passed=result.passed,
        total_tests=result.total_tests,
        passed_tests=result.passed_tests,
        results=results,
        duration_ms=result.duration_ms,
        error=result.error,
        newly_solved=newly_solved,
    )
