from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="EcoAudio Mapper API", validation_alias="APP_NAME")
    environment: str = Field(default="development", validation_alias="ENVIRONMENT")
    debug: bool = Field(default=False, validation_alias="DEBUG")
    api_v1_prefix: str = Field(default="/api/v1", validation_alias="API_V1_PREFIX")
    enable_docs: bool = Field(default=True, validation_alias="ENABLE_DOCS")
    database_url: str = Field(
        default="sqlite+pysqlite:///./ecoaudio_mapper.db",
        validation_alias="DATABASE_URL",
    )
    alembic_database_url: str | None = Field(default=None, validation_alias="ALEMBIC_DATABASE_URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def effective_alembic_database_url(self) -> str:
        return self.alembic_database_url or self.database_url


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
