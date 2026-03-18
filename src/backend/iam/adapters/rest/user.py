from fastapi import APIRouter, status, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from adapters.rest.database import get_db_session
from typing import Annotated
from usecases.user import UserService
from domain.models.user import User
from repository.postgresql.user import UserRepositoryPostgres
from adapters.auth.hasher import PasswordHasher

router = APIRouter(prefix="/users", tags=["users"])

class BaseUserRequest(BaseModel):
    email: str
    password: str

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


def get_user_service(session: Annotated[AsyncSession, Depends(get_db_session)]) -> UserService:
    return UserService(repository=UserRepositoryPostgres(session))

def get_hasher() -> PasswordHasher:
    return PasswordHasher()


@router.get(path="/v1", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(
    service: Annotated[UserService, Depends(get_user_service)],
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
) -> list[UserResponse]:
    return await service.get_users(offset=offset, limit=limit)


@router.post(path="/v1", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def add_user(user: CreateUserRequest,
                   service: Annotated[UserService, Depends(get_user_service)],
                   hasher: Annotated[PasswordHasher, Depends(get_hasher)]
                   ) -> UserResponse:
    domain_user = User(
        company_id=user.company_id,
        email=user.email,
        password_hash=hasher.get_password_hash(user.password),
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

    return request

@router.post(path="/v1/admin", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def add_admin(user: BaseUserRequest,
                   service: Annotated[UserService, Depends(get_user_service)],
                   hasher: Annotated[PasswordHasher, Depends(get_hasher)]
                   ) -> UserResponse:
    domain_user = User(
        company_id=None,
        email=user.email,
        password_hash=hasher.get_password_hash(user.password),
        first_name=user.first_name,
        last_name=user.last_name,
        telegram_username=user.telegram_username,
        avatar_url=user.avatar_url,
        role="ADMIN",
        is_active=True
    )
    request = await service.add_user(domain_user)
    if request is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже есть в базе"
        )

    return request

@router.post(path="/v1/company_admin", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def add_company_admin(user: CreateUserRequest,
                   service: Annotated[UserService, Depends(get_user_service)],
                   hasher: Annotated[PasswordHasher, Depends(get_hasher)]
                   ) -> UserResponse:
    domain_user = User(
        company_id=user.company_id,
        email=user.email,
        password_hash=hasher.get_password_hash(user.password),
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

    return request

@router.delete(path="/v1/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int,
        service: Annotated[UserService, Depends(get_user_service)]
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
        new_user: CreateUserRequest,
        service: Annotated[UserService, Depends(get_user_service)],
        hasher: Annotated[PasswordHasher, Depends(get_hasher)]
    ) -> UserResponse:
    domain_user = User(
        company_id=new_user.company_id,
        email=new_user.email,
        password_hash=hasher.get_password_hash(new_user.password),
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

    return request
