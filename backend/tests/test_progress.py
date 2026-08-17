CORRECT_FACTORIAL = "def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)\n"


def test_progress_starts_empty(client):
    resp = client.get("/api/progress")
    assert resp.status_code == 200
    data = resp.json()
    assert data["solved_exercises"] == 0
    assert data["completion_pct"] == 0.0
    assert data["current_streak"] == 0
    assert data["next_recommended"] is not None
    assert len(data["topic_mastery"]) >= 6


def test_progress_updates_after_solve(client):
    client.post(
        "/api/exercises/recursion-01-factorial/submit",
        json={"code": CORRECT_FACTORIAL, "mode": "submit"},
    )
    data = client.get("/api/progress").json()
    assert data["solved_exercises"] == 1
    assert data["completion_pct"] > 0
    recursion_topic = next(t for t in data["topic_mastery"] if t["topic"] == "recursion")
    assert recursion_topic["solved"] == 1


def test_ai_status_disabled_without_key(client):
    resp = client.get("/api/ai/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["enabled"] is False


def test_ai_generate_exercise_503_without_key(client):
    resp = client.post("/api/ai/generate-exercise", json={"topic": "loops", "difficulty": "beginner"})
    assert resp.status_code == 503
