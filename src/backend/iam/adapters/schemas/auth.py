from pydantic import BaseModel


class AuthUser(BaseModel):
    email: str
    password: str
    company_slug: str | None = None


class LoginResponse(BaseModel):
    message: str
    role: str