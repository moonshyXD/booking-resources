from shared.config.base import ConfigBase
from pydantic.types import SecretStr
from pydantic_settings import SettingsConfigDict


class JWTConfig(ConfigBase):
    model_config = SettingsConfigDict(
        env_prefix="JWT_",
    )

    secret_key: SecretStr
    algorithm: SecretStr
    expires_in: int