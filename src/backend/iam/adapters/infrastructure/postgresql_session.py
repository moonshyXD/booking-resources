from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from adapters.config.settings import Config


class PostgresDependency:
    def __init__(self) -> None:
        config = Config.load()
        db_url = f"postgresql+asyncpg://{config.db.user.get_secret_value()}:{config.db.password.get_secret_value()}@{config.db.host}/{config.db.database}"

        self._engine = create_async_engine(
            db_url,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
        )
        self._session_factory = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def get_db_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.get_session() as session:
            yield session

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()