from fastapi import APIRouter, status, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Annotated

from adapters.infrastructure.postgresql_session import PostgresDependency

from usecases.user import UserService
from domain.models.user import User
from repository.orm.user import UserRepositoryPostgres
from adapters.auth.hasher import PasswordHasher
from adapters.infrastructure.logger import logging
from adapters.shared.role import RoleChecker

router = APIRouter(prefix="/users", tags=["users"])

require_admin = RoleChecker(["ADMIN"])
require_admin_or_company_admin = RoleChecker(["ADMIN", "COMPANY_ADMIN"])

db_obj = PostgresDependency()

class BaseUserRequest(BaseModel):
    email: str
    first_name: str | None = None
    last_name: str | None = None
    telegram_username: str | None = None
    avatar_url: str | None = None


class CreateUserRequest(BaseUserRequest):
    company_id: int


class UpdateUserRequest(CreateUserRequest):
    role: str


class UserResponse(BaseModel):
    id: int
    company_id: int | None
    email: str
    first_name: str | None = None
    last_name: str | None = None
    telegram_username: str | None = None
    avatar_url: str | None = None
    role: str
    is_active: bool
    created_at: datetime


def get_user_service(session: Annotated[AsyncSession, Depends(db_obj.get_db_session)]) -> UserService:
    return UserService(repository=UserRepositoryPostgres(session))


def get_hasher() -> PasswordHasher:
    return PasswordHasher()


@router.get(path="/v1", response_model=list[UserResponse], status_code=status.HTTP_200_OK, dependencies=[Depends(require_admin)])
async def get_users(
        service: Annotated[UserService, Depends(get_user_service)],
        offset: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=100),
) -> list[UserResponse]:
    return await service.get_users(offset=offset, limit=limit)


@router.post(path="/v1", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def add_user(
        user: CreateUserRequest,
        service: Annotated[UserService, Depends(get_user_service)],
        hasher: Annotated[PasswordHasher, Depends(get_hasher)],
        current_user: dict = Depends(require_admin_or_company_admin)
) -> UserResponse:
    if current_user.get("role") == "COMPANY_ADMIN":
        if user.company_id != current_user.get("company_id"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы можете добавлять пользователей только в свою компанию"
            )
    password = hasher.get_password()
    domain_user = User(
        company_id=user.company_id,
        email=user.email,
        password_hash=hasher.get_password_hash(password),
        first_name=user.first_name,
        last_name=user.last_name,
        telegram_username=user.telegram_username,
        avatar_url=user.avatar_url,
        role="USER",
        is_active=True
    )
    request = await service.add_user(domain_user)
    if request is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже есть в базе или указана несуществующая компания"
        )

    logging.info(f"Сгенерированный пароль пользователя: {password}")
    return request


@router.post(path="/v1/company_admin", response_model=UserResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
async def add_company_admin(
        user: CreateUserRequest,
        service: Annotated[UserService, Depends(get_user_service)],
        hasher: Annotated[PasswordHasher, Depends(get_hasher)],
) -> UserResponse:
    password = hasher.get_password()
    domain_user = User(
        company_id=user.company_id,
        email=user.email,
        password_hash=hasher.get_password_hash(password),
        first_name=user.first_name,
        last_name=user.last_name,
        telegram_username=user.telegram_username,
        avatar_url=user.avatar_url,
        role="COMPANY_ADMIN",
        is_active=True
    )
    request = await service.add_user(domain_user)
    if request is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже есть в базе или указана несуществующая компания"
        )

    logging.info(f"Сгенерированный пароль пользователя: {password}")
    return request


@router.delete(path="/v1/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin_or_company_admin)])
async def delete_user(
        user_id: int,
        service: Annotated[UserService, Depends(get_user_service)],
):
    request = await service.delete_user(user_id)
    if request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )


@router.put(path="/v1/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(
        user_id: int,
        new_user: UpdateUserRequest,
        service: Annotated[UserService, Depends(get_user_service)],
        hasher: Annotated[PasswordHasher, Depends(get_hasher)],
        current_user: dict = Depends(require_admin_or_company_admin)
) -> UserResponse:
    if current_user.get("role") == "COMPANY_ADMIN":
        if new_user.company_id != current_user.get("company_id"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы можете взаимодействовать только со своей компанией"
            )
    password = hasher.get_password()
    domain_user = User(
        company_id=new_user.company_id,
        email=new_user.email,
        password_hash=hasher.get_password_hash(password),
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        telegram_username=new_user.telegram_username,
        avatar_url=new_user.avatar_url,
        role=new_user.role,
        is_active=True
    )
    request = await service.update_user(user_id, domain_user)
    if request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )

    logging.info(f"Сгенерированный пароль пользователя: {password}")
    return request