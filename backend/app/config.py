from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "JobBot AI"
    api_prefix: str = "/api"
    debug: bool = False
    database_url: str = Field(default="sqlite:///./jobbot.db")
    redis_url: str = Field(default="redis://localhost:6379/0")
    jwt_secret: str = Field(default="change-me-in-production")
    jwt_algorithm: str = "HS256"
    upload_dir: str = Field(default="/tmp/jobbot_uploads")
    openai_api_key: str = ""
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    max_upload_size_mb: int = 10

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, value):
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"release", "prod", "production", "false", "0", "no", "off"}:
                return False
            if normalized in {"debug", "dev", "development", "true", "1", "yes", "on"}:
                return True
        return value

    @property
    def cors_origins_list(self):
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = Path(get_settings().upload_dir)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
