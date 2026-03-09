from typing import Protocol


class PasswordHasherI(Protocol):
    def get_password_hash(self, password: str) -> str: ...

    def verify_password(
        self, plain_password: str, hashed_password: str
    ) -> bool: ...
