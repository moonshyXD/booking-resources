from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass
class User:
    company_id: int
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
    async def delete_user_by_id(self, user: User) -> None: ...
    async def update_user_by_id(self, user_id: int, new_user: User) -> User: ...
    async def get_id_by_email(self, email: str) -> int: ...
    async def get_password_by_id(self, user_id: int) -> str | None: ...
