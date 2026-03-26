from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Response, Request

from iam.adapters.schemas.auth import AuthUser, LoginResponse

from iam.adapters.dependencies.auth import (
    get_auth_service,
    get_current_user_payload,
    get_blacklist_adapter
)

from iam.usecases.auth import AuthService
from shared.auth.blacklist import TokenBlacklistAdapter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(path="/v1/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(
        user: AuthUser,
        service: Annotated[AuthService, Depends(get_auth_service)],
        response: Response
) -> LoginResponse:
    tokens = await service.authenticate(
        email=user.email,
        password=user.password,
        company_slug=user.company_slug
    )

    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email, пароль или организация"
        )

    response.set_cookie(
        key="access_token", value=tokens["access_token"],
        httponly=True, secure=True, samesite="lax", max_age=3600, path="/"
    )
    response.set_cookie(
        key="refresh_token", value=tokens["refresh_token"],
        httponly=True, secure=True, samesite="lax", max_age=30 * 24 * 3600, path="/"
    )

    return LoginResponse(
        message="Успешная авторизация",
        role=tokens["role"]
    )


@router.post(path="/v1/logout", status_code=status.HTTP_200_OK)
async def logout(
        request: Request,
        response: Response,
        blacklist: Annotated[TokenBlacklistAdapter, Depends(get_blacklist_adapter)],
        payload: dict = Depends(get_current_user_payload),
):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    if access_token:
        expire_timestamp = payload.get("exp")
        if expire_timestamp:
            await blacklist.add_token(access_token, expire_timestamp)
            await blacklist.add_token(refresh_token, expire_timestamp)

    response.delete_cookie("access_token", httponly=True, secure=True, samesite="lax", path="/")
    response.delete_cookie("refresh_token", httponly=True, secure=True, samesite="lax", path="/")

    return {"message": "Вы успешно вышли из системы"}