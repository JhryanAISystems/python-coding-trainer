"""Centralized app settings, loaded from environment variables / .env."""
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
EXERCISES_DIR = BASE_DIR / "exercises"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = f"sqlite:///{BASE_DIR / 'trainer.db'}"
    frontend_origin: str = "http://localhost:5173"

    anthropic_api_key: str | None = None
    openai_api_key: str | None = None

    sandbox_timeout_seconds: float = 5.0
    sandbox_memory_mb: int = 128

    rate_limit_per_minute: int = 30

    log_level: str = "INFO"

    @property
    def ai_enabled(self) -> bool:
        return bool(self.anthropic_api_key or self.openai_api_key)


@lru_cache
def get_settings() -> Settings:
    return Settings()
