from pydantic import EmailStr
from pydantic_settings import SettingsConfigDict
from shared.config.base import ConfigBase


class SMTPConfig(ConfigBase):
    server: str = "smtp.gmail.com"
    port: int = 465
    username: str
    password: str
    from_address: EmailStr
    subject: str = "Уведомление от Booking Resources"

    model_config = SettingsConfigDict(env_prefix="SMTP_")