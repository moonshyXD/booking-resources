import uuid
from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException, Query

from iam.adapters.dependencies.user import get_user_service, get_hasher
from iam.adapters.dependencies.auth import require_admin, require_admin_or_company_admin

from iam.adapters.schemas.user import (
    CreateUserRequest, UpdateUserRequest, UserResponse,
    BaseUserRequest, UpdatePasswordRequest
)

from iam.domain.models.user import User
from iam.domain.models.user_role import UserRole
from iam.usecases.user import UserService
from iam.adapters.auth.hasher import PasswordHasher
from shared.infrastructure.logger import logging

router = APIRouter(prefix="/users", tags=["users"])


def map_to_domain_user(request_data: BaseUserRequest, password_hash: str, role: str,
                       company_id: uuid.UUID | None = None) -> User:
    return User(
        company_id=company_id, email=request_data.email, password_hash=password_hash,
        first_name=request_data.first_name, last_name=request_data.last_name,
        avatar_url=request_data.avatar_url, role=role, is_active=True
    )


@router.get(path="/v1", response_model=list[UserResponse], dependencies=[Depends(require_admin)])
async def get_users(
        service: Annotated[UserService, Depends(get_user_service)],
        offset: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100),
) -> list[UserResponse]:
    return await service.get_users(offset=offset, limit=limit)


@router.post(path="/v1", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def add_user(
        user: CreateUserRequest,
        service: Annotated[UserService, Depends(get_user_service)],
        hasher: Annotated[PasswordHasher, Depends(get_hasher)],
        current_user: Annotated[dict, Depends(require_admin_or_company_admin)]
) -> UserResponse:
    if current_user.get("role") == UserRole.COMPANY_ADMIN:
        if str(user.company_id) != str(current_user.get("company_id")):
            raise HTTPException(status_code=403, detail="Доступ запрещен к чужой компании")

    password = hasher.get_password()
    domain_user = map_to_domain_user(user, hasher.get_password_hash(password), "USER", user.company_id)

    result = await service.add_user(domain_user)
    if result is None:
        raise HTTPException(status_code=409, detail="Ошибка создания пользователя")

    logging.info(f"Сгенерированный пароль: {password}")
    return result


@router.post(path="/v1/admin", response_model=UserResponse, dependencies=[Depends(require_admin)])
async def add_admin(
        user: BaseUserRequest,
        service: Annotated[UserService, Depends(get_user_service)],
        hasher: Annotated[PasswordHasher, Depends(get_hasher)]
) -> UserResponse:
    password = hasher.get_password()
    domain_user = map_to_domain_user(user, hasher.get_password_hash(password), UserRole.ADMIN)

    result = await service.add_user(domain_user)
    if result is None:
        raise HTTPException(status_code=409, detail="Админ уже существует")

    logging.info(f"Сгенерированный пароль админа: {password}")
    return result


@router.post(path="/v1/company_admin", response_model=UserResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_admin)])
async def add_company_admin(
        user: CreateUserRequest,
        service: Annotated[UserService, Depends(get_user_service)],
        hasher: Annotated[PasswordHasher, Depends(get_hasher)],
) -> UserResponse:
    password = hasher.get_password()
    domain_user = map_to_domain_user(
        request_data=user, 
        password_hash=hasher.get_password_hash(password), 
        role=UserRole.COMPANY_ADMIN, 
        company_id=user.company_id
    )
    
    result = await service.add_user(domain_user)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже есть в базе или указана несуществующая компания"
        )

    logging.info(f"Сгенерированный пароль администратора компании: {password}")
    return result


@router.delete(path="/v1/{user_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_admin_or_company_admin)])
async def delete_user(
        user_id: uuid.UUID,
        service: Annotated[UserService, Depends(get_user_service)],
):
    result = await service.delete_user(user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")


@router.put(path="/v1/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(
        user_id: uuid.UUID,
        new_user: UpdateUserRequest,
        service: Annotated[UserService, Depends(get_user_service)],
        current_user: Annotated[dict, Depends(require_admin_or_company_admin)]
) -> UserResponse:
    if current_user.get("role") == UserRole.COMPANY_ADMIN:
        if str(new_user.company_id) != str(current_user.get("company_id")):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Вы можете взаимодействовать только со своей компанией"
            )
            
    existing_password_hash = await service.repository.get_password_by_id(user_id)
    if existing_password_hash is None:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    domain_user = map_to_domain_user(
        request_data=new_user, 
        password_hash=existing_password_hash, 
        role=new_user.role, 
        company_id=new_user.company_id
    )
    
    request = await service.update_user(user_id, domain_user)
    if request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )

    return request


@router.patch(path="/v1/password", response_model=UserResponse)
async def update_password(
        request_data: UpdatePasswordRequest,
        service: Annotated[UserService, Depends(get_user_service)],
        hasher: Annotated[PasswordHasher, Depends(get_hasher)],
) -> UserResponse:
    user_id = await service.repository.get_id_by_email(request_data.email)
    if not user_id:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    password = hasher.get_password()
    updated_user = await service.update_password(user_id, hasher.get_password_hash(password))

    logging.info(f"Новый пароль для {user_id}: {password}")
    return updated_user
