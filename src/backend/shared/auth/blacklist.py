from datetime import datetime, timezone
from redis.asyncio import Redis

class TokenBlacklistAdapter:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    async def add_token(self, token: str, expire_timestamp: int) -> None:
        now = int(datetime.now(timezone.utc).timestamp())
        ttl_seconds = expire_timestamp - now

        if ttl_seconds > 0:
            await self.redis.setex(f"blacklist:{token}", ttl_seconds, "revoked")

    async def is_blacklisted(self, token: str) -> bool:
        exists = await self.redis.exists(f"blacklist:{token}")
        return exists > 0