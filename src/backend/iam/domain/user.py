from dataclasses import dataclass
from datetime import time
from typing import Protocol


@dataclass
class User:
    id: int
    company_id: int
    email: str
    password_hash: str
    first_name: str
    second_name: str
    role: str
    is_active: bool
    created_at: time


class UserRepositoryI(Protocol):
    def get_user(self, user: User): ...
    def add_user(self, user: User): ...
    def delete_user(self, user: User): ...
    def update_user(self, user: User, new_user: User): ...
