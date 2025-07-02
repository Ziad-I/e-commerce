from typing import AsyncGenerator
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.elastic.lifespan import init_elasticsearch, close_elasticsearch
from app.rabbitmq.lifespan import init_rabbitmq, close_rabbitmq


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
    await init_elasticsearch(app)
    await init_rabbitmq(app)
    try:
        yield
    finally:
        await close_elasticsearch(app)
        await close_rabbitmq(app)
