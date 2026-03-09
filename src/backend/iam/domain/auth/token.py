from typing import Protocol


class TokenProviderI(Protocol):
    def create_access_token(self, data: dict) -> str: ...
