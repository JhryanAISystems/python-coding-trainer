"""FastAPI application entrypoint: CORS, routers, error handling, logging."""
import logging
import time

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from app.config import get_settings
from app.database import Base, engine
from app.rate_limit import limiter
from app.routers import ai_tutor, exercises, progress, submissions

settings = get_settings()

logging.basicConfig(
    level=settings.log_level,
    format='{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","msg":%(message)r}',
)
logger = logging.getLogger("app")

# Dev convenience: create tables if they don't exist yet. For production
# schema changes, use Alembic ("alembic upgrade head") instead.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Python Coding Trainer API",
    description="Backend for an interactive Python exercise trainer with sandboxed grading.",
    version="1.0.0",
)

app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    duration_ms = int((time.perf_counter() - started) * 1000)
    logger.info("%s %s -> %d (%dms)", request.method, request.url.path, response.status_code, duration_ms)
    return response


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Too many requests. Please slow down and try again shortly."},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid request.", "errors": exc.errors()},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred."},
    )


app.include_router(exercises.router)
app.include_router(submissions.router)
app.include_router(progress.router)
app.include_router(ai_tutor.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
