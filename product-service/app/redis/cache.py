from loguru import logger
from redis.asyncio import Redis
from app.core.config import settings


def get_product_cache_key(product_id: str) -> str:
    """
    Generate a cache key for a product based on its ID.

    Args:
        product_id (str): The ID of the product.

    Returns:
        str: The cache key for the product.
    """
    return f"product:{product_id}"


async def set_product_cache(redis: Redis, product_id: str, product_data: dict) -> None:
    """
    Set the cache for a product.

    Args:
        redis (Redis): The Redis client.
        product_id (str): The ID of the product.
        product_data (dict): The product data to cache.
    """
    cache_key = get_product_cache_key(product_id)
    await redis.set(cache_key, product_data, ex=settings.REDIS_CACHE_EXPIRE)
    logger.info(f"Product {product_id} cached with key {cache_key}.")


async def get_product_cache(redis: Redis, product_id: str) -> dict | None:
    """
    Get the cached product data.

    Args:
        redis (Redis): The Redis client.
        product_id (str): The ID of the product.

    Returns:
        dict | None: The cached product data or None if not found.
    """
    cache_key = get_product_cache_key(product_id)
    cached_data = await redis.get(cache_key)
    if cached_data:
        return cached_data
    return None


async def delete_product_cache(redis: Redis, product_id: str) -> None:
    """
    Delete the cached product data.

    Args:
        redis (Redis): The Redis client.
        product_id (str): The ID of the product.
    """
    cache_key = get_product_cache_key(product_id)
    await redis.delete(cache_key)
    logger.info(f"Product {product_id} cache deleted with key {cache_key}.")
