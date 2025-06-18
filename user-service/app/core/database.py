from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import AsyncGenerator

from app.core.config import settings
from app.models import User


async def init_db(app: FastAPI) -> None:
    """
    Connect to MongoDB via Motor, initialize Beanie with our Document models.

    Args:
        app (FastAPI): FastAPI application instance.
    """
    client = AsyncIOMotorClient(
        settings.mongodb_url,
    )

    await init_beanie(
        database=client.get_default_database(),
        document_models=[User],  # list all your Document classes here
    )

    app.state.mongo_client = client


async def close_db(app: FastAPI) -> None:
    """
    Closes database connection pool.

    Args:
        app (FastAPI): fastAPI application.
    """
    client: AsyncIOMotorClient = app.state.mongo_client
    client.close()
