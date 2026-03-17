from src.backend.iam.adapters.config.base import ConfigBase
from pydantic_settings import SettingsConfigDict


class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="DB_")

    host: str
    password: str
