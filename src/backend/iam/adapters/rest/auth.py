from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from adapters.auth.hasher import PasswordHasher
from adapters.auth.token import TokenProvider
from usecases.auth import AuthService
from repository.postgresql.user import UserRepositoryPostgres
from adapters.config.settings import Config
from adapters.rest.database import get_db_session


router = APIRouter(prefix="/auth")

class AuthUser(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    role: str
    type: str = "bearer"


def get_auth_service(session: Annotated[AsyncSession, Depends(get_db_session)]) -> AuthService:
    return AuthService(
        hasher=PasswordHasher(),
        token_provider=TokenProvider(),
        repository=UserRepositoryPostgres(session)
    )

@router.post(path="/v1/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
        user: AuthUser, service: Annotated[AuthService, Depends(get_auth_service)]
) -> TokenResponse:
    tokens = await service.authenticate(email=user.email, password=user.password)

    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )

    return tokens