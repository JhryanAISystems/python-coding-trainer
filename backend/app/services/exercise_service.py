"""Loads exercise definitions from YAML files under backend/exercises/.

Exercises are the source of truth on disk (not the database) so new ones can
be added by dropping in a YAML file -- no code changes, no migration.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache

import yaml

from app.config import EXERCISES_DIR

DIFFICULTY_ORDER = {"beginner": 0, "intermediate": 1, "advanced": 2}


@dataclass
class Exercise:
    id: str
    title: str
    topic: str
    difficulty: str
    order: int
    description: str
    function_name: str
    starter_code: str
    solution: str
    hints: list[str] = field(default_factory=list)
    test_cases: list[dict] = field(default_factory=list)

    @classmethod
    def from_yaml(cls, path) -> "Exercise":
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        required = ["id", "title", "topic", "difficulty", "description", "function_name", "starter_code", "test_cases"]
        missing = [k for k in required if k not in data]
        if missing:
            raise ValueError(f"{path}: missing required fields {missing}")
        return cls(
            id=data["id"],
            title=data["title"],
            topic=data["topic"],
            difficulty=data["difficulty"],
            order=data.get("order", 0),
            description=data["description"],
            function_name=data["function_name"],
            starter_code=data["starter_code"],
            solution=data.get("solution", ""),
            hints=data.get("hints", [])[:3],
            test_cases=data["test_cases"],
        )


class ExerciseNotFoundError(KeyError):
    pass


@lru_cache
def _load_all() -> dict[str, Exercise]:
    exercises: dict[str, Exercise] = {}
    for path in sorted(EXERCISES_DIR.glob("*.yaml")):
        ex = Exercise.from_yaml(path)
        if ex.id in exercises:
            raise ValueError(f"Duplicate exercise id '{ex.id}' in {path}")
        exercises[ex.id] = ex
    return exercises


def list_exercises() -> list[Exercise]:
    return sorted(
        _load_all().values(),
        key=lambda e: (e.topic, DIFFICULTY_ORDER.get(e.difficulty, 9), e.order, e.id),
    )


def get_exercise(exercise_id: str) -> Exercise:
    try:
        return _load_all()[exercise_id]
    except KeyError as exc:
        raise ExerciseNotFoundError(exercise_id) from exc


def list_topics() -> list[str]:
    topics = sorted({e.topic for e in _load_all().values()})
    return topics


def reload_cache() -> None:
    """Used by tests / hot-reload to force re-reading YAML from disk."""
    _load_all.cache_clear()
