from fastapi import APIRouter, Depends, status, HTTPException, Response
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


class LoginResponse(BaseModel):
    message: str
    role: str


def get_auth_service(session: Annotated[AsyncSession, Depends(get_db_session)]) -> AuthService:
    return AuthService(
        hasher=PasswordHasher(),
        token_provider=TokenProvider(),
        repository=UserRepositoryPostgres(session)
    )


@router.post(path="/v1/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(
        user: AuthUser,
        service: Annotated[AuthService, Depends(get_auth_service)],
        response: Response
) -> LoginResponse:
    tokens = await service.authenticate(email=user.email, password=user.password)

    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )

    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600
    )

    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=30 * 24 * 3600
    )

    return LoginResponse(
        message="Успешная авторизация",
        role=tokens["role"]
    )
