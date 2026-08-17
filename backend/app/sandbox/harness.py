"""Trusted grading harness, executed as a *separate OS process* to run
untrusted, learner-submitted code.

Isolation model (documented honestly -- see README "Security & sandboxing"
for the full writeup):

  - The submission is never passed through ``eval``/``exec`` of a shell
    string, and never runs via ``shell=True``. The parent process
    (``app/sandbox/runner.py``) writes the user's code to a plain ``.py``
    file inside a throwaway temp directory and launches *this* trusted
    script as a fresh Python subprocess with that directory as its cwd.
  - Wall-clock timeout is enforced by the parent process via
    ``subprocess.run(..., timeout=...)`` (cross-platform).
  - On POSIX, the parent additionally applies CPU-time and address-space
    (memory) rlimits via ``resource.setrlimit`` in a ``preexec_fn`` before
    the interpreter even starts. Windows has no rlimit equivalent exposed
    to Python, so on Windows only the wall-clock timeout applies -- this is
    a known, documented limitation.
  - Before importing the submission, this harness disables ``socket.socket``
    (blocking network access) and wraps ``open``/``io.open`` so any file
    access outside the scratch directory raises ``PermissionError``.

This is defense-in-depth appropriate for a local coding-practice tool, not
a hard multi-tenant security boundary. For untrusted internet-scale use,
run this inside a real container/VM sandbox (gVisor, Firecracker, Docker
with ``--network=none`` and a read-only rootfs) in addition to the above.
"""
import builtins
import contextlib
import io
import json
import os
import traceback

WORKDIR = os.getcwd()


def _lockdown() -> None:
    import socket

    def _blocked_socket(*_args, **_kwargs):
        raise PermissionError("Network access is disabled in the sandbox")

    socket.socket = _blocked_socket  # type: ignore[assignment]

    real_open = builtins.open

    def _guarded_open(file, *args, **kwargs):
        try:
            path = os.path.abspath(os.fspath(file))
        except TypeError:
            return real_open(file, *args, **kwargs)
        if not (path == WORKDIR or path.startswith(WORKDIR + os.sep)):
            raise PermissionError("Filesystem access is restricted to the sandbox scratch dir")
        return real_open(file, *args, **kwargs)

    builtins.open = _guarded_open  # type: ignore[assignment]
    io.open = _guarded_open  # type: ignore[assignment]


def _to_repr(value, limit: int = 2000) -> str:
    try:
        text = repr(value)
    except Exception:
        text = "<unrepresentable>"
    return text if len(text) <= limit else text[:limit] + "...(truncated)"


def _normalize(value):
    """Test cases round-trip through JSON, so tuples become lists and dict
    keys become strings on the 'expected' side (JSON object keys are always
    strings). Normalize both sides the same way before comparing so a
    function that legitimately returns a tuple or non-string-keyed dict
    isn't marked wrong."""
    if isinstance(value, (tuple, list)):
        return [_normalize(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _normalize(v) for k, v in value.items()}
    return value


def main() -> None:
    _lockdown()

    with open("testcases.json") as f:
        spec = json.load(f)

    function_name = spec["function_name"]
    test_cases = spec["test_cases"]

    namespace: dict = {"__name__": "submission"}

    try:
        with open("submission.py") as f:
            source = f.read()
        code_obj = compile(source, "submission.py", "exec")
        exec(code_obj, namespace)
    except Exception:
        err = traceback.format_exc(limit=3)
        print(json.dumps({"fatal_error": f"Error loading your code:\n{err}"}))
        return

    func = namespace.get(function_name)
    if not callable(func):
        print(json.dumps({"fatal_error": f"Function '{function_name}' was not defined."}))
        return

    results = []
    for case in test_cases:
        name = case.get("name", "case")
        args = case.get("args", [])
        kwargs = case.get("kwargs", {})
        expected = case.get("expected")
        expect_error = case.get("expect_error", False)
        error_type = case.get("error_type")
        stdout_buf = io.StringIO()
        entry = {"name": name, "input_repr": _to_repr({"args": args, "kwargs": kwargs})}
        try:
            with contextlib.redirect_stdout(stdout_buf):
                actual = func(*args, **kwargs)
            if expect_error:
                entry["passed"] = False
                entry["actual_repr"] = _to_repr(actual)
                entry["expected_repr"] = f"raises {error_type or 'an exception'}"
                entry["error"] = "Expected an exception to be raised, but none was."
            else:
                entry["actual_repr"] = _to_repr(actual)
                entry["expected_repr"] = _to_repr(expected)
                entry["passed"] = _normalize(actual) == _normalize(expected)
                entry["error"] = None
            entry["stdout"] = stdout_buf.getvalue()[:2000]
        except Exception as exc:
            entry["stdout"] = stdout_buf.getvalue()[:2000]
            if expect_error:
                type_ok = error_type is None or type(exc).__name__ == error_type
                entry["passed"] = type_ok
                entry["actual_repr"] = f"raised {type(exc).__name__}: {exc}"
                entry["expected_repr"] = f"raises {error_type or 'an exception'}"
                entry["error"] = None if type_ok else f"Expected {error_type}, got {type(exc).__name__}"
            else:
                entry["passed"] = False
                entry["actual_repr"] = None
                entry["expected_repr"] = _to_repr(expected)
                entry["error"] = traceback.format_exc(limit=2)
        results.append(entry)

    print(json.dumps({"results": results}))


if __name__ == "__main__":
    main()
