from pydantic import BaseModel

class RedisConfig(BaseModel):
    host: str
    port: int


class FastapiConfig(BaseModel):
    host: str
    port: int
