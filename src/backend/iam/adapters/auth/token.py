from datetime import datetime, timedelta, timezone
import jwt
from adapters.config.settings import Config

config = Config.load()


class TokenProvider:
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire_minutes = config.jwt.expires_in
        time_delta = timedelta(minutes=expire_minutes)
        secret_key = config.jwt.secret_key.get_secret_value()
        algorithm = config.jwt.algorithm.get_secret_value()
        if time_delta:
            expire = datetime.now(timezone.utc) + time_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
        return encoded_jwt
