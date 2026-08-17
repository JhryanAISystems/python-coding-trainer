CORRECT_FACTORIAL = "def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)\n"
WRONG_FACTORIAL = "def factorial(n):\n    return n\n"


def test_run_correct_solution(client):
    resp = client.post(
        "/api/exercises/recursion-01-factorial/submit",
        json={"code": CORRECT_FACTORIAL, "mode": "run"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["passed"] is True
    assert data["passed_tests"] == data["total_tests"]


def test_run_incorrect_solution_shows_diff(client):
    resp = client.post(
        "/api/exercises/recursion-01-factorial/submit",
        json={"code": WRONG_FACTORIAL, "mode": "run"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["passed"] is False
    failing = [r for r in data["results"] if not r["passed"]]
    assert len(failing) > 0
    assert failing[0]["expected_repr"] is not None
    assert failing[0]["actual_repr"] is not None


def test_submit_persists_and_marks_solved(client):
    resp = client.post(
        "/api/exercises/recursion-01-factorial/submit",
        json={"code": CORRECT_FACTORIAL, "mode": "submit"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["passed"] is True
    assert data["newly_solved"] is True

    detail = client.get("/api/exercises/recursion-01-factorial").json()
    assert detail["solved"] is True

    progress = client.get("/api/progress").json()
    assert progress["solved_exercises"] >= 1
    assert progress["current_streak"] >= 1


def test_submit_unknown_exercise_404(client):
    resp = client.post(
        "/api/exercises/nope/submit",
        json={"code": "x = 1", "mode": "run"},
    )
    assert resp.status_code == 404


def test_submit_rejects_empty_code(client):
    resp = client.post(
        "/api/exercises/recursion-01-factorial/submit",
        json={"code": "", "mode": "run"},
    )
    assert resp.status_code == 422
