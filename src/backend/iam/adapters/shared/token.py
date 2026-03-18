import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from iam.adapters.auth.token import TokenProvider

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/v1/login")

token_provider = TokenProvider()


async def get_current_user_payload(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = token_provider.verify_access_token(token)
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Время действия токена истекло. Авторизуйтесь заново",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен авторизации",
            headers={"WWW-Authenticate": "Bearer"},
        )