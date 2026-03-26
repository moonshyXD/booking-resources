from typing import Self
from pydantic import Field
from pydantic_settings import BaseSettings, TomlConfigSettingsSource
from shared.config.redis import RedisConfig
from shared.config.web import FastapiConfig
from notifications.adapters.config.smtp import SMTPConfig
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config(BaseSettings):
    redis: RedisConfig
    fastapi: FastapiConfig
    smtp: SMTPConfig = Field(default_factory=SMTPConfig)

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
            TomlConfigSettingsSource(settings_cls, BASE_DIR / "config.toml"),
            file_secret_settings,
        )

    @classmethod
    def load(cls) -> Self:
        return cls()

