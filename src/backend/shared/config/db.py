from shared.config.base import ConfigBase
from pydantic.types import SecretStr
from pydantic_settings import SettingsConfigDict

class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(
        env_prefix="POSTGRES_",
    )

    host: str
    password: SecretStr
    user: SecretStr
    database: str
