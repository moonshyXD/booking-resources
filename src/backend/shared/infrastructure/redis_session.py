from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from redis.asyncio import ConnectionPool, Redis

class RedisDependency:
    def __init__(self, redis_url: str) -> None:
        self._url = redis_url
        self._pool: ConnectionPool = self._init_pool()

    def _init_pool(self) -> ConnectionPool:
        return ConnectionPool.from_url(
            url=self._url, encoding="utf-8", decode_responses=True
        )

    async def get_redis_session(self) -> AsyncGenerator[Redis, None]:
        async with self.get_client() as client:
            yield client

    @asynccontextmanager
    async def get_client(self) -> AsyncGenerator[Redis, None]:
        redis_client = Redis(connection_pool=self._pool)
        try:
            yield redis_client
        finally:
            await redis_client.aclose()