# Hyperion
# Copyright (C) 2025 Arian Ott <arian.ott@ieee.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
from typing import AsyncIterator

import redis.asyncio as redis

from . import settings

logger = logging.getLogger("hyperion.redis")


class RedisManager:
    """
    Manages the Redis connection pool and client factory.

    This class ensures that a single connection pool is initialised and shared
    across the application, minimising overhead and managing resource lifecycles.
    """

    def __init__(self):
        """
        Initialise the RedisManager.

        Loads the Redis URL from environment variables or defaults to localhost.
        """
        self.redis_url = settings.REDIS_URL
        self.pool: redis.ConnectionPool | None = None

    def connect(self):
        """
        Create the connection pool.

        Should be called on application startup.
        """
        try:
            self.pool = redis.ConnectionPool.from_url(
                self.redis_url, decode_responses=True
            )
            logger.info("✅ Redis connection pool created")
        except Exception as e:
            logger.error(f"🔥 Failed to connect to Redis: {e}")
            raise e

    async def close(self):
        """
        Close the connection pool.

        Should be called on application shutdown.
        """
        if self.pool:
            await self.pool.disconnect()
            logger.info("🛑 Redis connection pool closed")

    def get_client(self) -> redis.Redis:
        """
        Create a new Redis client using the shared pool.

        :return: An active Redis client instance.
        :rtype: redis.Redis
        """
        if not self.pool:
            raise RuntimeError("Redis pool is not initialised. Call connect() first.")
        return redis.Redis(connection_pool=self.pool)


redis_manager = RedisManager()


async def get_redis() -> AsyncIterator[redis.Redis]:
    """
    Dependency to provide a Redis client for a request lifecycle.

    This yields a client from the pool and ensures it is properly closed
    after the request is processed.

    :yield: An active Redis client.
    :rtype: AsyncIterator[redis.Redis]
    """
    client = redis_manager.get_client()
    try:
        yield client
    finally:
        await client.aclose()
