def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_list_exercises(client):
    resp = client.get("/api/exercises")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["exercises"]) >= 20
    assert len(data["topics"]) >= 6
    assert all("solved" in e for e in data["exercises"])


def test_filter_by_topic(client):
    resp = client.get("/api/exercises", params={"topic": "recursion"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["exercises"]) > 0
    assert all(e["topic"] == "recursion" for e in data["exercises"])


def test_filter_by_difficulty(client):
    resp = client.get("/api/exercises", params={"difficulty": "beginner"})
    assert resp.status_code == 200
    data = resp.json()
    assert all(e["difficulty"] == "beginner" for e in data["exercises"])


def test_get_exercise_detail(client):
    resp = client.get("/api/exercises/recursion-01-factorial")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == "recursion-01-factorial"
    assert data["function_name"] == "factorial"
    assert data["hint_count"] >= 1
    assert "starter_code" in data


def test_get_exercise_not_found(client):
    resp = client.get("/api/exercises/does-not-exist")
    assert resp.status_code == 404


def test_get_hint(client):
    resp = client.get("/api/exercises/recursion-01-factorial/hints/0")
    assert resp.status_code == 200
    data = resp.json()
    assert data["hint_index"] == 0
    assert isinstance(data["hint"], str) and data["hint"]


def test_get_hint_out_of_range(client):
    resp = client.get("/api/exercises/recursion-01-factorial/hints/99")
    assert resp.status_code == 404
