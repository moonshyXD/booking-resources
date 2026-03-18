from datetime import datetime, timedelta, timezone
import jwt
from pydantic import BaseModel
from adapters.config.settings import Config

config = Config.load()

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenProvider:
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire_minutes = config.jwt.expires_in
        time_delta = timedelta(minutes=expire_minutes) if expire_minutes else timedelta(minutes=15)

        secret_key = config.jwt.secret_key.get_secret_value()
        algorithm = config.jwt.algorithm.get_secret_value()

        expire = datetime.now(timezone.utc) + time_delta
        to_encode.update({"exp": expire, "type": "access"})

        return jwt.encode(to_encode, secret_key, algorithm=algorithm)

    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        time_delta = timedelta(days=30)

        secret_key = config.jwt.secret_key.get_secret_value()
        algorithm = config.jwt.algorithm.get_secret_value()

        expire = datetime.now(timezone.utc) + time_delta
        to_encode.update({"exp": expire, "type": "refresh"})

        return jwt.encode(to_encode, secret_key, algorithm=algorithm)

    def decode_token(self, token: str) -> dict:
        secret_key = config.jwt.secret_key.get_secret_value()
        algorithm = config.jwt.algorithm.get_secret_value()

        return jwt.decode(token, secret_key, algorithms=[algorithm])

    def verify_access_token(self, token: str) -> dict:
        payload = self.decode_token(token)

        if payload.get("type") != "access":
            raise jwt.InvalidTokenError("Ожидался access токен, но получен другой тип")

        return payload

    def verify_refresh_token(self, token: str) -> dict:
        payload = self.decode_token(token)

        if payload.get("type") != "refresh":
            raise jwt.InvalidTokenError("Ожидался refresh токен, но получен другой тип")

        return payload