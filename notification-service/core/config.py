import enum
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class LogLevel(str, enum.Enum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    APP_ENV: str = "development"
    PROJECT_NAME: str = "Notification Service"

    LOG_LEVEL: LogLevel = LogLevel.INFO

    # gRPC Settings
    NOTIFICATION_SERVICE_GRPC_HOST: str = "0.0.0.0"
    NOTIFICATION_SERVICE_GRPC_PORT: int = 50051

    # SMTP Settings
    SMTP_HOST: str = "smtp.mailtrap.io"
    SMTP_PORT: int = 465
    SMTP_FROM: str = "noreply@example.com"
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_USER: str = "your_mailtrap_username"
    SMTP_PASSWORD: str = "your_mailtrap_password"

    TEMPLATES_DIR: str = "./templates"

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
