"""SQLAlchemy ORM models. This is a single-user local app (no auth/login),
so progress rows aren't scoped to a user_id -- they represent "your" history.
"""
from datetime import datetime, date, timezone

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Attempt(Base):
    """A single run/submit of code against an exercise."""

    __tablename__ = "attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exercise_id: Mapped[str] = mapped_column(String(64), index=True)
    code: Mapped[str] = mapped_column(Text)
    mode: Mapped[str] = mapped_column(String(16))  # "run" | "submit"
    passed: Mapped[bool] = mapped_column(Boolean, default=False)
    total_tests: Mapped[int] = mapped_column(Integer, default=0)
    passed_tests: Mapped[int] = mapped_column(Integer, default=0)
    results_json: Mapped[dict] = mapped_column(JSON, default=list)
    duration_ms: Mapped[int] = mapped_column(Integer, default=0)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), index=True
    )


class Solve(Base):
    """Aggregate state per exercise: first-solved timestamp + attempt counters."""

    __tablename__ = "solves"

    exercise_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    solved: Mapped[bool] = mapped_column(Boolean, default=False)
    first_solved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    times_attempted: Mapped[int] = mapped_column(Integer, default=0)
    times_passed: Mapped[int] = mapped_column(Integer, default=0)
    hints_used: Mapped[int] = mapped_column(Integer, default=0)


class StreakDay(Base):
    """One row per calendar day with at least one submit attempt (for streak calc)."""

    __tablename__ = "streak_days"

    day: Mapped[date] = mapped_column(Date, primary_key=True)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    solves: Mapped[int] = mapped_column(Integer, default=0)
