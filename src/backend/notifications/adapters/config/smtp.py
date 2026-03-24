from pydantic import BaseModel

class SMTPConfig(BaseModel):
    user: str
    password: str
    host: str = "smtp.gmail.com"
    port: int = 465