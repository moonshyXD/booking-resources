from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from redis.asyncio import ConnectionPool, Redis
from adapters.config.settings import Config


class RedisDependency:
    def __init__(self) -> None:
        config = Config.load()
        self._url = config.redis.url
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