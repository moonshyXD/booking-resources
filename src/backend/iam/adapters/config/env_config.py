from adapters.config.base import ConfigBase
from pydantic.types import SecretStr
from pydantic_settings import SettingsConfigDict


class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="POSTGRES_")

    host: str
    password: SecretStr
    user: SecretStr
    database: str


class IamConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="IAM_")


class JWTConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="JWT_")

    secret_key: SecretStr
    algorithm: SecretStr
    expires_in: int