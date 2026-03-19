from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyCookie
import jwt
from adapters.auth.token import TokenProvider

cookie_scheme = APIKeyCookie(name="access_token", auto_error=False)
token_provider = TokenProvider()

async def get_current_user_payload(token: str = Depends(cookie_scheme)) -> dict:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Отсутствует токен авторизации",
        )
    try:
        return token_provider.verify_access_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен")

