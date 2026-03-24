from typing import Self

from pydantic_settings import BaseSettings, TomlConfigSettingsSource

from shared.config.redis import RedisConfig
from shared.config.web import FastapiConfig
from adapters.config.smtp import SMTPConfig


class Config(BaseSettings):
    redis: RedisConfig
    fastapi: FastapiConfig
    smtp: SMTPConfig

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
            TomlConfigSettingsSource(settings_cls, "config.toml"),
            file_secret_settings,
        )

    @classmethod
    def load(cls) -> Self:
        return cls()

