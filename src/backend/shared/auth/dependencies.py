from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis

from shared.auth.token import TokenVerifier
from shared.auth.blacklist import TokenBlacklistAdapter

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/v1/login", auto_error=False)


async def get_token_from_request(
        request: Request,
        token_from_header: str = Depends(oauth2_scheme)
) -> str:
    if token_from_header:
        return token_from_header

    token_from_cookie = request.cookies.get("access_token")
    if token_from_cookie:
        return token_from_cookie

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Токен не найден ни в заголовках, ни в куках"
    )


def setup_auth_dependencies(secret_key: str, algorithm: str, get_redis_session_func):
    verifier = TokenVerifier(secret_key=secret_key, algorithm=algorithm)

    async def get_blacklist_adapter(
            redis_client: Redis = Depends(get_redis_session_func)
    ) -> TokenBlacklistAdapter:
        return TokenBlacklistAdapter(redis_client=redis_client)

    async def get_current_user_payload(
            token: str = Depends(get_token_from_request),
            blacklist: TokenBlacklistAdapter = Depends(get_blacklist_adapter)
    ) -> dict:
        if await blacklist.is_blacklisted(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен отозван"
            )
        return verifier.verify_access_token(token)

    return get_current_user_payload, get_blacklist_adapter