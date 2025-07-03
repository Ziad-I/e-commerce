from loguru import logger
from fastapi import FastAPI

from app.rabbitmq.rabbit import get_rabbitmq_client


async def init_rabbitmq(app: FastAPI):
    """Initialize RabbitMQ connection."""
    rabbitmq_client = get_rabbitmq_client()
    app.state.rabbitmq = rabbitmq_client
    await rabbitmq_client.connect()
    logger.info("RabbitMQ client initialized and connected.")


async def close_rabbitmq(app: FastAPI):
    """Close RabbitMQ connection."""
    if hasattr(app.state, "rabbitmq"):
        await app.state.rabbitmq.close()
    logger.info("RabbitMQ client closed.")
