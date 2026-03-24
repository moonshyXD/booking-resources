from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from iam.usecases.user import UserService
from iam.repository.orm.user import UserRepositoryPostgres
from iam.adapters.auth.hasher import PasswordHasher

from iam.adapters.dependencies.general import get_db_session

def get_user_service(session: Annotated[AsyncSession, Depends(get_db_session)]) -> UserService:
    return UserService(repository=UserRepositoryPostgres(session))

def get_hasher() -> PasswordHasher:
    return PasswordHasher()