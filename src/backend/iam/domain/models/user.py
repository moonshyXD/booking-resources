from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass
class User:
    company_id: int | None
    email: str
    password_hash: str

    id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    telegram_username: str | None = None
    avatar_url: str | None = None
    role: str = "USER"
    is_active: bool = True
    created_at: datetime | None = None


class UserRepositoryI(Protocol):
    async def get_user_by_id(self, user_id: int) -> User | None: ...
    async def add_user(self, user: User) -> User: ...
    async def delete_user_by_id(self, user_id: int) -> User | None: ...
    async def update_user_by_id(self, user_id: int, new_user: User) -> User | None: ...
    async def get_id_by_email(self, email: str) -> int | None: ...
    async def get_password_by_id(self, user_id: int) -> str | None: ...
    async def get_users(self, offset: int = 0, limit: int = 20) -> list[User]: ...
    async def get_role_by_id(self, user_id: int) -> str | None: ...
    async def get_user_by_email(self, email: str) -> User | None: ...