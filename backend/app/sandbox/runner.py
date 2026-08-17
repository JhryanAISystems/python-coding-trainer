"""Spawns app/sandbox/harness.py as a subprocess to grade a submission.

See harness.py's module docstring for the full isolation model. This module
owns: scratch-dir lifecycle, resource limits (POSIX), the wall-clock
timeout, and translating the harness's JSON stdout into typed results.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

HARNESS_PATH = Path(__file__).resolve().parent / "harness.py"


@dataclass
class SandboxResult:
    passed: bool
    total_tests: int
    passed_tests: int
    results: list[dict] = field(default_factory=list)
    duration_ms: int = 0
    error: str | None = None


def _posix_preexec_fn(memory_mb: int, cpu_seconds: float):
    def _limit():
        import resource

        mem_bytes = memory_mb * 1024 * 1024
        try:
            resource.setrlimit(resource.RLIMIT_AS, (mem_bytes, mem_bytes))
        except (ValueError, OSError):
            pass
        cpu_limit = max(1, int(cpu_seconds) + 1)
        try:
            resource.setrlimit(resource.RLIMIT_CPU, (cpu_limit, cpu_limit))
        except (ValueError, OSError):
            pass
        try:
            resource.setrlimit(resource.RLIMIT_NPROC, (32, 32))
        except (ValueError, OSError, AttributeError):
            pass
        try:
            resource.setrlimit(resource.RLIMIT_FSIZE, (5 * 1024 * 1024, 5 * 1024 * 1024))
        except (ValueError, OSError):
            pass

    return _limit


def _minimal_env() -> dict:
    env = {"PATH": os.environ.get("PATH", ""), "PYTHONIOENCODING": "utf-8"}
    if os.name == "nt":
        for key in ("SYSTEMROOT", "WINDIR", "TEMP", "TMP", "PATHEXT"):
            if key in os.environ:
                env[key] = os.environ[key]
    return env


def run_submission(
    code: str,
    function_name: str,
    test_cases: list[dict],
    timeout_seconds: float,
    memory_mb: int,
) -> SandboxResult:
    started = time.perf_counter()

    with tempfile.TemporaryDirectory(prefix="pytrainer_") as tmp:
        tmp_path = Path(tmp)
        (tmp_path / "submission.py").write_text(code, encoding="utf-8")
        (tmp_path / "testcases.json").write_text(
            json.dumps({"function_name": function_name, "test_cases": test_cases}),
            encoding="utf-8",
        )

        kwargs: dict = {}
        if os.name == "posix":
            kwargs["preexec_fn"] = _posix_preexec_fn(memory_mb, timeout_seconds)

        try:
            proc = subprocess.run(
                [sys.executable, str(HARNESS_PATH)],
                cwd=str(tmp_path),
                env=_minimal_env(),
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                **kwargs,
            )
        except subprocess.TimeoutExpired:
            duration_ms = int((time.perf_counter() - started) * 1000)
            return SandboxResult(
                passed=False,
                total_tests=len(test_cases),
                passed_tests=0,
                error=f"Your code timed out after {timeout_seconds:.0f}s (infinite loop or too slow).",
                duration_ms=duration_ms,
            )

        duration_ms = int((time.perf_counter() - started) * 1000)

        if proc.returncode != 0 and not proc.stdout.strip():
            stderr_tail = (proc.stderr or "").strip()[-1500:]
            return SandboxResult(
                passed=False,
                total_tests=len(test_cases),
                passed_tests=0,
                error=stderr_tail or "The sandbox process exited unexpectedly (likely a resource limit).",
                duration_ms=duration_ms,
            )

        try:
            payload = json.loads(proc.stdout.strip().splitlines()[-1])
        except (json.JSONDecodeError, IndexError):
            return SandboxResult(
                passed=False,
                total_tests=len(test_cases),
                passed_tests=0,
                error="Could not parse sandbox output.",
                duration_ms=duration_ms,
            )

        if "fatal_error" in payload:
            return SandboxResult(
                passed=False,
                total_tests=len(test_cases),
                passed_tests=0,
                error=payload["fatal_error"],
                duration_ms=duration_ms,
            )

        results = payload["results"]
        passed_tests = sum(1 for r in results if r["passed"])
        return SandboxResult(
            passed=passed_tests == len(results) and len(results) > 0,
            total_tests=len(results),
            passed_tests=passed_tests,
            results=results,
            duration_ms=duration_ms,
        )
