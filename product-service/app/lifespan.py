from typing import AsyncGenerator
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import close_db, init_db
from app.redis.lifespan import close_redis, init_redis
from app.rabbitmq.lifespan import close_rabbitmq, init_rabbitmq


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    Args:
        app (FastAPI): the fastAPI application.

    Returns:
        function that actually performs actions.
    """
    await init_db(app)
    await init_redis(app)
    await init_rabbitmq(app)
    try:
        yield
    finally:
        await close_db(app)
        await close_redis(app)
        await close_rabbitmq(app)
