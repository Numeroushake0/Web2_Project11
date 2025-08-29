import redis.asyncio as redis
from app.core.config import settings

redis_client = redis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}")


async def set_cache(key: str, value: str, expire: int = 600):
    """
    Set a value in Redis cache with expiration.

    Args:
        key (str): Cache key.
        value (str): Value to store.
        expire (int, optional): Expiration time in seconds. Default is 600.
    """
    await redis_client.set(key, value, ex=expire)


async def get_cache(key: str):
    """
    Retrieve a value from Redis cache.

    Args:
        key (str): Cache key.

    Returns:
        str | None: Cached value if exists, else None.
    """
    return await redis_client.get(key)


async def delete_cache(key: str):
    """
    Delete a key from Redis cache.

    Args:
        key (str): Cache key to delete.
    """
    await redis_client.delete(key)
