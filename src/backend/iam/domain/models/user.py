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
    def get_user_by_id(self, user_id: int) -> User | None: ...
    def add_user(self, user: User) -> User: ...
    def delete_user_by_id(self, user: User) -> None: ...
    def update_user_by_id(self, user_id: int, new_user: User) -> User: ...
