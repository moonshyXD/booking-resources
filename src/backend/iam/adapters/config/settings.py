from typing import Self

from pydantic import Field
from pydantic_settings import BaseSettings, TomlConfigSettingsSource

from adapters.config.env_config import DatabaseConfig, JWTConfig
from adapters.config.toml_config import FastapiConfig, RedisConfig


class Config(BaseSettings):
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    jwt: JWTConfig = Field(default_factory=JWTConfig)
    redis: RedisConfig
    fastapi: FastapiConfig

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            TomlConfigSettingsSource(settings_cls, "settings/config.toml"),
            file_secret_settings,
        )

    @classmethod
    def load(cls) -> Self:
        return cls()
