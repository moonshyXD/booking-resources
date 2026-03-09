from datetime import datetime, timedelta, timezone

import jwt
from decouple import config


class TokenProvider:
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire_minutes = config("IAM_ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)
        time_delta = timedelta(minutes=expire_minutes)
        secret_key = config("IAM_SECRET_KEY")
        algorithm = config("IAM_ALGORITHM")
        if time_delta:
            expire = datetime.now(timezone.utc) + time_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
        return encoded_jwt
