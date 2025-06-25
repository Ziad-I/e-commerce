from fastapi import Request
from redis.asyncio import Redis


async def get_redis(request: Request) -> Redis:
    """
    Dependency function that provides a Redis client.

    Args:
        request: FastAPI request object
    Returns:
        client: Redis client instance from the app state
    """
    return request.app.state.redis
