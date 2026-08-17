"""Pydantic request/response schemas."""
from datetime import datetime, date

from pydantic import BaseModel, Field


# ---------- Exercises ----------

class ExerciseSummary(BaseModel):
    id: str
    title: str
    topic: str
    difficulty: str
    order: int
    solved: bool = False
    times_attempted: int = 0


class ExerciseDetail(BaseModel):
    id: str
    title: str
    topic: str
    difficulty: str
    description: str
    starter_code: str
    function_name: str
    hint_count: int
    solved: bool = False
    times_attempted: int = 0


class ExerciseListResponse(BaseModel):
    exercises: list[ExerciseSummary]
    topics: list[str]


class HintResponse(BaseModel):
    exercise_id: str
    hint_index: int
    hint: str
    hints_remaining: int


# ---------- Submissions ----------

class SubmitRequest(BaseModel):
    code: str = Field(min_length=1, max_length=20_000)
    mode: str = Field(default="run", pattern="^(run|submit)$")


class TestCaseResult(BaseModel):
    name: str
    passed: bool
    input_repr: str
    expected_repr: str
    actual_repr: str | None = None
    error: str | None = None
    stdout: str | None = None


class SubmitResponse(BaseModel):
    exercise_id: str
    mode: str
    passed: bool
    total_tests: int
    passed_tests: int
    results: list[TestCaseResult]
    duration_ms: int
    error: str | None = None
    newly_solved: bool = False


# ---------- Progress ----------

class TopicMastery(BaseModel):
    topic: str
    solved: int
    total: int
    mastery_pct: float


class ProgressPoint(BaseModel):
    day: date
    attempts: int
    solves: int


class ProgressResponse(BaseModel):
    total_exercises: int
    solved_exercises: int
    completion_pct: float
    current_streak: int
    longest_streak: int
    total_attempts: int
    topic_mastery: list[TopicMastery]
    history: list[ProgressPoint]
    next_recommended: ExerciseSummary | None = None


# ---------- AI tutor ----------

class GenerateExerciseRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=64)
    difficulty: str = Field(default="beginner", pattern="^(beginner|intermediate|advanced)$")


class GeneratedExercise(BaseModel):
    title: str
    description: str
    starter_code: str
    function_name: str


class CodeReviewRequest(BaseModel):
    exercise_id: str
    code: str = Field(min_length=1, max_length=20_000)


class CodeReviewResponse(BaseModel):
    review: str


class AIStatusResponse(BaseModel):
    enabled: bool
    provider: str | None = None


# ---------- Errors ----------

class ErrorResponse(BaseModel):
    detail: str
