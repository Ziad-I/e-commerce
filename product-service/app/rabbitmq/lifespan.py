from loguru import logger
import aio_pika
from fastapi import FastAPI
from aio_pika import Channel
from aio_pika.abc import AbstractChannel, AbstractRobustConnection
from aio_pika.pool import Pool

from app.core.config import settings


async def init_rabbitmq(app: FastAPI) -> None:
    """
    Initialize rabbitmq pools.

    Args:
        app (FastAPI): FastAPI application instance.
    """

    async def get_connection() -> AbstractRobustConnection:
        """
        Creates connection to RabbitMQ using url from settings.

        Returns:
            AbstractRobustConnection: An instance of AbstractRobustConnection,
        """
        return await aio_pika.connect_robust(str(settings.rabbitmq_url))

    async def get_channel() -> AbstractChannel:
        """
        Open channel on connection.
        Channels are used to actually communicate with rabbitmq.

        Returns:
            AbstractChannel: An instance of AbstractChannel, the connected channel.
        """
        async with connection_pool.acquire() as connection:
            return await connection.channel()

    connection_pool: Pool[AbstractRobustConnection] = Pool(get_connection)
    channel_pool: Pool[Channel] = Pool(get_channel)

    app.state.rmq_pool = connection_pool
    app.state.rmq_channel_pool = channel_pool
    logger.info("Connected to RabbitMQ.")


async def close_rabbitmq(app: FastAPI) -> None:
    """
    Close all connection and pools.

    Args:
        app (FastAPI): FastAPI application instance.
    """
    await app.state.rmq_channel_pool.close()
    await app.state.rmq_pool.close()
    logger.info("Closed RabbitMQ connections.")
