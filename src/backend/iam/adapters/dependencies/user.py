from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from iam.usecases.user import UserService
from iam.repository.orm.user import UserRepositoryPostgres
from iam.adapters.auth.hasher import PasswordHasher
from iam.adapters.notifications.gateway import NotificationRedisGateway

from iam.adapters.dependencies.general import get_db_session
from iam.adapters.config.settings import Config


config = Config.load()

def get_user_service(session: Annotated[AsyncSession, Depends(get_db_session)]) -> UserService:
    return UserService(
        repository=UserRepositoryPostgres(session),
        hasher=PasswordHasher(),
        notifications=NotificationRedisGateway(config.redis.url)
    )

def get_hasher() -> PasswordHasher:
    return PasswordHasher()