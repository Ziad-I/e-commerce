import os
import secrets
from typing import Optional
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL
import enum


class LogLevel(str, enum.Enum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    # General settings
    APP_ENV: str = "development"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Search Service"

    # Logging settings
    LOG_LEVEL: LogLevel = LogLevel.INFO

    # MongoDB settings
    MONGODB_SCHEME: str
    MONGODB_USER: Optional[str] = None
    MONGODB_PASSWORD: Optional[str] = None
    MONGODB_HOST: str = "localhost"
    MONGODB_PORT: Optional[int] = 27017
    MONGODB_DB: str
    MONGODB_URI: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def mongodb_url(self) -> str:
        """
        Return a MongoDB connection URL using yarl.URL.

        Priority:
            1) MONGODB_URI (as is, if fully specified in env)
            2) Constructed from parts using yarl.URL
        """
        if self.MONGODB_URI:
            return self.MONGODB_URI

        # Build MongoDB URL using yarl
        return str(
            URL.build(
                scheme=self.MONGODB_SCHEME,
                user=self.MONGODB_USER,
                password=self.MONGODB_PASSWORD,
                host=self.MONGODB_HOST,
                port=(
                    self.MONGODB_PORT if self.MONGODB_SCHEME != "mongodb+srv" else None
                ),
                path=f"/{self.MONGODB_DB}",
            )
        )


@lru_cache()
def get_settings() -> Settings:
    """Get settings."""
    return Settings()


settings = get_settings()
