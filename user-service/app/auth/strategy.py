from fastapi_users.authentication import JWTStrategy
from app.core.config import settings


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.ACCESS_TOKEN_SECRET,
        lifetime_seconds=settings.ACCESS_TOKEN_LIFETIME_SECONDS,
    )


def get_refresh_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.REFRESH_TOKEN_SECRET,
        lifetime_seconds=settings.REFRESH_TOKEN_LIFETIME_SECONDS,
    )
