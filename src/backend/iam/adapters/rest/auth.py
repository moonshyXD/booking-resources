from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from adapters.auth.hasher import PasswordHasher
from adapters.auth.token import TokenProvider
from usecases.auth import AuthService
from repository.orm.user import UserRepositoryPostgres
from adapters.config.settings import Config
from adapters.infrastructure.postgresql_session import PostgresDependency

from adapters.shared.token import get_current_user_payload

from adapters.infrastructure.redis.blacklist import TokenBlacklistAdapter

router = APIRouter(prefix="/auth", tags=["auth"])

db_obj = PostgresDependency()

class AuthUser(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    message: str
    role: str


def get_auth_service(session: Annotated[AsyncSession, Depends(db_obj.get_db_session)]) -> AuthService:
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


@router.post(path="/v1/logout", status_code=status.HTTP_200_OK)
async def logout(
        request: Request,
        response: Response,
        payload: dict = Depends(get_current_user_payload),
        blacklist: TokenBlacklistAdapter = Depends(TokenBlacklistAdapter)
):
    access_token = request.cookies.get("access_token")

    if access_token:
        expire_timestamp = payload.get("exp")

        if expire_timestamp:
            await blacklist.add_token(access_token, expire_timestamp)

    response.delete_cookie("access_token", httponly=True, secure=True, samesite="lax")
    response.delete_cookie("refresh_token", httponly=True, secure=True, samesite="lax")

    return {"message": "Вы успешно вышли из системы"}