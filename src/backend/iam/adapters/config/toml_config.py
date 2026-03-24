from pydantic import BaseModel

class RedisConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: int = 0

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"

class FastapiConfig(BaseModel):
    host: str
    port: int
