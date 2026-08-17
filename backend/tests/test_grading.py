import pytest

from app.sandbox.runner import run_submission
from app.services import exercise_service


@pytest.mark.parametrize("exercise", exercise_service.list_exercises(), ids=lambda e: e.id)
def test_reference_solution_passes(exercise):
    """Every bundled exercise's own reference solution must pass its own tests."""
    result = run_submission(
        code=exercise.solution,
        function_name=exercise.function_name,
        test_cases=exercise.test_cases,
        timeout_seconds=5.0,
        memory_mb=128,
    )
    assert result.passed, f"{exercise.id} solution failed: {result.error or result.results}"
    assert result.total_tests == len(exercise.test_cases)
    assert result.passed_tests == result.total_tests


def test_starter_code_does_not_pass():
    """Sanity check: the unfinished starter stub should fail, not accidentally pass."""
    exercise = exercise_service.get_exercise("recursion-01-factorial")
    result = run_submission(
        code=exercise.starter_code,
        function_name=exercise.function_name,
        test_cases=exercise.test_cases,
        timeout_seconds=5.0,
        memory_mb=128,
    )
    assert result.passed is False


def test_syntax_error_reports_fatal_error():
    result = run_submission(
        code="def broken(:\n    pass",
        function_name="broken",
        test_cases=[{"name": "x", "args": [], "expected": None}],
        timeout_seconds=5.0,
        memory_mb=128,
    )
    assert result.passed is False
    assert result.error is not None


def test_infinite_loop_times_out():
    code = "def loopy():\n    while True:\n        pass\n"
    result = run_submission(
        code=code,
        function_name="loopy",
        test_cases=[{"name": "x", "args": [], "expected": None}],
        timeout_seconds=1.0,
        memory_mb=128,
    )
    assert result.passed is False
    assert "timed out" in (result.error or "").lower()


def test_network_access_is_blocked():
    code = (
        "import socket\n"
        "def try_connect():\n"
        "    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n"
        "    return 'connected'\n"
    )
    result = run_submission(
        code=code,
        function_name="try_connect",
        test_cases=[{"name": "x", "args": [], "expected": "connected"}],
        timeout_seconds=5.0,
        memory_mb=128,
    )
    assert result.passed is False
    assert result.results[0]["passed"] is False


def test_filesystem_access_outside_scratch_is_blocked():
    code = (
        "def try_read():\n"
        "    with open('/etc/passwd') as f:\n"
        "        return f.read()\n"
    )
    result = run_submission(
        code=code,
        function_name="try_read",
        test_cases=[{"name": "x", "args": [], "expected": "n/a"}],
        timeout_seconds=5.0,
        memory_mb=128,
    )
    assert result.passed is False
