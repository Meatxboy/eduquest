from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    bot_token: str = "123456:TESTTOKEN"
    environment: str = "development"
    backend_base_url: str = "http://backend:8000"
    frontend_base_url: str = "https://example.com/app"
    webhook_url: str | None = None
    webhook_secret: str | None = None
    redis_url: str = "redis://redis:6379/1"

    def is_placeholder_token(self) -> bool:
        token = (self.bot_token or "").strip()
        return not token or token.endswith(":TESTTOKEN")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
