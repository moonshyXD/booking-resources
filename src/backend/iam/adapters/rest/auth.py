from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from adapters.auth.hasher import PasswordHasher
from adapters.auth.token import TokenProvider
from usecases.auth import AuthService
from repository.postgresql.user import UserRepositoryPostgres
from adapters.infrastructure.postgresql_session import DatabaseDependency
from adapters.config.settings import Config

router = APIRouter(prefix="/auth")

class AuthUser(BaseModel):
    email: str
    password: str


config = Config.load()
db_url = f"postgresql+asyncpg://{config.db.user.get_secret_value()}:{config.db.password.get_secret_value()}@{config.db.host}/{config.db.database}"
db_dependency = DatabaseDependency(db_url)

async def get_db_session():
    async with db_dependency.get_session() as session:
        yield session

def get_auth_service(session: Annotated[AsyncSession, Depends(get_db_session)]):
    return AuthService(
        hasher=PasswordHasher(),
        token_provider=TokenProvider(),
        repository=UserRepositoryPostgres(session)
    )

@router.post(path="/v1/login", status_code=status.HTTP_200_OK)
async def login(
    user: AuthUser, service: Annotated[AuthService, Depends(get_auth_service)]
) -> str | None:
    return await service.authenticate(email=user.email, password=user.password)
