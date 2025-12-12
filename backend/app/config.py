from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application configuration using pydantic-settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Application metadata
    app_name: str = "HeroAccounts Receipt AI"
    app_version: str = "1.0.0"
    app_description: str = "AI-powered receipt intake, validation, and workflow automation."

    # Database & persistence
    database_url: str = Field(
        default="postgresql+psycopg://postgreys:int%40123@localhost:5432/hero_db"
    )

    # CORS / Frontend
    frontend_origins: List[str] = Field(default_factory=lambda: ["http://localhost:5173"])

    # Notifications (SMTP)
    smtp_host: str = Field(default="smtp.gmail.com")
    smtp_port: int = Field(default=587)
    smtp_user: str = Field(default="")
    smtp_pass: str = Field(default="")

    # Legacy / extra environment keys (ignored but accepted)
    secret_key: str = Field(default="replace_with_secure_value")
    AI_SECRET_KEY: str = Field(default="")
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached Settings instance."""
    return Settings()

