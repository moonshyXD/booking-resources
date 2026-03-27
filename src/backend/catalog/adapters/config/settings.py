from pathlib import Path
from typing import Self

from pydantic import Field
from pydantic_settings import BaseSettings, TomlConfigSettingsSource

from shared.config.redis import RedisConfig
from shared.config.web import FastapiConfig
from shared.config.jwt import JWTConfig
from shared.config.db import DatabaseConfig

BASE_DIR = Path(__file__).resolve().parent


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
        config_path = BASE_DIR / "config.toml"

        return (
            init_settings,
            env_settings,
            dotenv_settings,
            TomlConfigSettingsSource(settings_cls, config_path),
            file_secret_settings,
        )

    @classmethod
    def load(cls) -> Self:
        return cls()
