from typing import AsyncGenerator
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.elastic.lifespan import init_elasticsearch, close_elasticsearch


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
    try:
        yield
    finally:
        await close_elasticsearch(app)
