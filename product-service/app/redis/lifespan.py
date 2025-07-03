from loguru import logger
from fastapi import FastAPI
from redis.asyncio import Redis

from app.core.config import settings


async def init_redis(app: FastAPI) -> None:
    """
    Creates Redis client and stores it in the app state.

    Args:
        app (FastAPI): fastAPI application.
    """
    redis = Redis.from_url(
        str(settings.redis_url),
        decode_responses=True,
    )
    app.state.redis = redis
    logger.info("Connected to Redis.")


async def close_redis(app: FastAPI) -> None:
    """
    Closes Redis client.

    Args:
        app (FastAPI): fastAPI application.
    """
    await app.state.redis.close()
    logger.info("Closed Redis connection.")
