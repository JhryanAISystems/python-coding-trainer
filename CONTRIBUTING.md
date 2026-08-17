# Contributing

Thanks for considering a contribution! This is a small project, so the
process is intentionally lightweight.

## Local setup

See the [README](README.md#getting-started) for full setup instructions —
either `docker-compose up` or running the backend/frontend separately.

## Adding a new exercise

Exercises live as individual YAML files under `backend/exercises/`. Adding
one doesn't require touching any application code:

1. Copy an existing file in `backend/exercises/` as a template.
2. Fill in `id`, `title`, `topic`, `difficulty`, `order`, `description`
   (markdown), `starter_code`, `function_name`, `solution`, `hints`
   (1-3 progressive hints), and `test_cases`.
3. Make sure `solution` actually passes every test case in `test_cases` —
   `backend/tests/test_grading.py` asserts this automatically for every
   exercise in the directory, so just running the backend test suite will
   catch mistakes.
4. If a test case's expected value needs to raise an exception instead of
   returning a value, use `expect_error: true` (optionally with
   `error_type: SomeExceptionName`) instead of `expected`.

## Running tests

```bash
# Backend
cd backend
pip install -r requirements.txt
pytest

# Frontend
cd frontend
npm install
npm test
npm run lint
```

## Pull requests

- Keep PRs focused — one feature or fix at a time.
- Make sure `pytest` and `npm test` both pass, and `npm run build` succeeds.
- Describe what changed and why in the PR description.

## Code style

- Backend: standard PEP 8, type hints where practical.
- Frontend: TypeScript, functional components, Tailwind for styling.

No formal style guide beyond "match what's already there."
