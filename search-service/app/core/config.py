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

    # Elasticsearch settings
    ELASTICSEARCH_HOST: URL = URL("http://localhost:9200")
    ELASTICSEARCH_INDEX: str = "products"
    ELASTICSEARCH_USER: str = "elastic"
    ELASTICSEARCH_PASSWORD: str = "elastic"

    # RabbitMQ settings
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"
    RABBITMQ_VHOST: str = "/"
    RABBITMQ_URI: Optional[str] = None
    RABBITMQ_EXCHANGE_NAME: str = "product_exchange"

    model_config = SettingsConfigDict(env_file=".env")

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
            path=f"/{self.RABBITMQ_VHOST}",
        )


@lru_cache()
def get_settings() -> Settings:
    """Get settings."""
    return Settings()


settings = get_settings()
