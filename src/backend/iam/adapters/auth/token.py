from datetime import datetime, timedelta, timezone
import jwt
from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    uuid: str
    token_type: str = "bearer"


class TokenProvider:
    def __init__(self, secret_key: str, algorithm: str, expires_in: int = 15):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires_in = expires_in

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()

        time_delta = timedelta(minutes=self.expires_in)
        expire = datetime.now(timezone.utc) + time_delta
        to_encode.update({"exp": expire, "type": "access"})

        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        time_delta = timedelta(days=30)

        expire = datetime.now(timezone.utc) + time_delta
        to_encode.update({"exp": expire, "type": "refresh"})

        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)