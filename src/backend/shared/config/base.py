from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


current_dir = Path(__file__).parent
env_path = current_dir / ".env"

class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_path, env_file_encoding="utf-8", extra="ignore"
    )
