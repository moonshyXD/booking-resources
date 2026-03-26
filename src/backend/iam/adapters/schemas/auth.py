from pydantic import BaseModel, EmailStr


class AuthUser(BaseModel):
    email: EmailStr
    password: str
    company_slug: str | None = None


class LoginResponse(BaseModel):
    message: str
    role: str