from shared.config.base import ConfigBase
from pydantic.types import SecretStr
from pydantic_settings import SettingsConfigDict
from pathlib import Path

current_dir = Path(__file__).parent
env_path = current_dir / ".env"

class JWTConfig(ConfigBase):
    model_config = SettingsConfigDict(
        env_prefix="JWT_",
    )

    secret_key: SecretStr
    algorithm: SecretStr
    expires_in: int