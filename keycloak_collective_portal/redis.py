"""Redis cache."""

import json

from aioredis import create_redis_pool


class Redis:
    """Redis cache."""

    def __init__(self):
        """Initialise the object."""
        self._redis = None

    async def create_pool(self, conn):
        """Initialise pool."""
        self._redis = await create_redis_pool(conn)
        return self

    async def keys(self, pattern):
        """Retrieve keys that match a pattern."""
        return await self._redis.keys(pattern)

    async def set(self, key, value, dumps=True):
        """Set a key."""
        if dumps:
            return await self._redis.set(key, json.dumps(value))
        return await self._redis.set(key, value)

    async def get(self, key, loads=True):
        """Get a specific key."""
        if loads:
            return json.loads(await self._redis.get(key))
        return await self._redis.get(key)

    async def close(self):
        """Close the connection."""
        self.redis_cache.close()
        await self.redis_cache.wait_closed()
