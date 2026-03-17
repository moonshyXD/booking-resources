from src.backend.iam.adapters.config.base import ConfigBase
from pydantic_settings import SettingsConfigDict


class IamConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="IAM_")
