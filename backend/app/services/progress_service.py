"""Computes dashboard-facing progress: completion, streaks, mastery, history."""
from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Solve, StreakDay
from app.schemas import ExerciseSummary, ProgressPoint, ProgressResponse, TopicMastery
from app.services.exercise_service import Exercise, list_exercises


def _solves_by_id(db: Session) -> dict[str, Solve]:
    return {s.exercise_id: s for s in db.scalars(select(Solve))}


def _compute_streaks(db: Session) -> tuple[int, int]:
    days = {row.day: row for row in db.scalars(select(StreakDay))}
    solved_days = sorted(d for d, row in days.items() if row.solves > 0)
    if not solved_days:
        return 0, 0

    longest = 1
    run = 1
    for prev, cur in zip(solved_days, solved_days[1:]):
        if cur - prev == timedelta(days=1):
            run += 1
        else:
            run = 1
        longest = max(longest, run)

    today = date.today()
    current = 0
    cursor = today
    solved_set = set(solved_days)
    if today not in solved_set:
        cursor = today - timedelta(days=1)
    while cursor in solved_set:
        current += 1
        cursor -= timedelta(days=1)

    return current, longest


def _history(db: Session, days: int = 30) -> list[ProgressPoint]:
    since = date.today() - timedelta(days=days - 1)
    rows = {row.day: row for row in db.scalars(select(StreakDay).where(StreakDay.day >= since))}
    points = []
    for i in range(days):
        d = since + timedelta(days=i)
        row = rows.get(d)
        points.append(ProgressPoint(day=d, attempts=row.attempts if row else 0, solves=row.solves if row else 0))
    return points


def _next_recommended(exercises: list[Exercise], solves: dict[str, Solve]) -> ExerciseSummary | None:
    for ex in exercises:
        solve = solves.get(ex.id)
        if not solve or not solve.solved:
            return ExerciseSummary(
                id=ex.id,
                title=ex.title,
                topic=ex.topic,
                difficulty=ex.difficulty,
                order=ex.order,
                solved=False,
                times_attempted=solve.times_attempted if solve else 0,
            )
    return None


def get_progress(db: Session) -> ProgressResponse:
    exercises = list_exercises()
    solves = _solves_by_id(db)

    solved_count = sum(1 for s in solves.values() if s.solved)
    total = len(exercises)
    completion_pct = round((solved_count / total) * 100, 1) if total else 0.0

    by_topic: dict[str, list[Exercise]] = {}
    for ex in exercises:
        by_topic.setdefault(ex.topic, []).append(ex)

    topic_mastery = []
    for topic, exs in sorted(by_topic.items()):
        solved_in_topic = sum(1 for e in exs if solves.get(e.id) and solves[e.id].solved)
        pct = round((solved_in_topic / len(exs)) * 100, 1) if exs else 0.0
        topic_mastery.append(TopicMastery(topic=topic, solved=solved_in_topic, total=len(exs), mastery_pct=pct))

    current_streak, longest_streak = _compute_streaks(db)
    total_attempts = sum(s.times_attempted for s in solves.values())

    return ProgressResponse(
        total_exercises=total,
        solved_exercises=solved_count,
        completion_pct=completion_pct,
        current_streak=current_streak,
        longest_streak=longest_streak,
        total_attempts=total_attempts,
        topic_mastery=topic_mastery,
        history=_history(db),
        next_recommended=_next_recommended(exercises, solves),
    )
