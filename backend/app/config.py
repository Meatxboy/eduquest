from functools import lru_cache
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "EduQuest Backend"
    environment: str = "development"

    database_url: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/eduquest"
    redis_url: str = "redis://redis:6379/0"

    telegram_bot_token: str = "123456:TESTTOKEN"
    telegram_webhook_secret: Optional[str] = None

    health_points_default: int = 100
    xp_per_level: int = 100

    cors_origins: list[str] | str | None = Field(
        default_factory=lambda: [
            "http://localhost:5173",
            "https://localhost:5173",
        ]
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: object) -> list[str]:
        if not value:
            return []
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        if isinstance(value, (list, tuple)):
            return [str(origin).strip() for origin in value if str(origin).strip()]
        raise ValueError("cors_origins must be a list or a comma-separated string")

    @property
    def cors_origins_list(self) -> list[str]:
        if isinstance(self.cors_origins, list):
            return self.cors_origins
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
        return []


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
