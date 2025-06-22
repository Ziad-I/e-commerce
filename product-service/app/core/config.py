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
    PROJECT_NAME: str = "Product Service"
    FRONTEND_URL: str = "http://localhost:5678"

    # Logging settings
    LOG_LEVEL: LogLevel = LogLevel.INFO

    # MongoDB settings
    MONGODB_SCHEME: str
    MONGODB_USER: Optional[str] = None
    MONGODB_PASSWORD: Optional[str] = None
    MONGODB_HOST: str = "localhost"
    MONGODB_PORT: Optional[int] = 27017
    MONGODB_DB: str
    MONGODB_URI: Optional[URL] = None

    # Redis settings
    REDIS_URL: Optional[URL] = None
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None

    # RabbitMQ settings
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"
    RABBITMQ_VHOST: str = "/"
    RABBITMQ_URI: Optional[URL] = None

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

    @property
    def redis_url(self) -> URL:
        """
        Return a Redis connection URL using yarl.URL.

        Priority:
            1) REDIS_URL (as is, if fully specified in env)
            2) Constructed from parts using yarl.URL
        """
        if self.REDIS_URL:
            return self.REDIS_URL

        return URL.build(
            scheme="redis",
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            password=self.REDIS_PASSWORD,
            path=f"/{self.REDIS_DB}",
        )

    @property
    def rabbitmq_url(self) -> URL:
        """
        Return a RabbitMQ connection URL using yarl.URL.

        Priority:
            1) RABBITMQ_URI (as is, if fully specified in env)
            2) Constructed from parts using yarl.URL
        """
        if self.RABBITMQ_URI:
            return self.RABBITMQ_URI

        return URL.build(
            scheme="amqp",
            user=self.RABBITMQ_USER,
            password=self.RABBITMQ_PASSWORD,
            host=self.RABBITMQ_HOST,
            port=self.RABBITMQ_PORT,
            path=self.RABBITMQ_VHOST,
        )


@lru_cache()
def get_settings() -> Settings:
    """Get settings."""
    return Settings()


settings = get_settings()
