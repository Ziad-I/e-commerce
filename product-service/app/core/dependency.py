from fastapi import Request
from aio_pika import Channel
from aio_pika.pool import Pool


async def get_redis(request: Request):
    """
    Dependency function that provides a Redis client.

    Args:
        request: FastAPI request object
    Returns:
        client: Redis client instance from the app state
    """
    return request.app.state.redis


def get_rmq_channel_pool(request: Request) -> Pool[Channel]:
    """
    Get channel pool from the state.

    Args:
        request: FastAPI request object
    Returns:
        Pool[Channel]: RabbitMQ channel pool from the app state
    """
    return request.app.state.rmq_channel_pool
