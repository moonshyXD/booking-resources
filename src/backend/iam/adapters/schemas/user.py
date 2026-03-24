from pydantic import BaseModel
import uuid
from datetime import datetime


class BaseUserRequest(BaseModel):
    email: str
    first_name: str | None = None
    last_name: str | None = None
    avatar_url: str | None = None


class CreateUserRequest(BaseUserRequest):
    company_id: uuid.UUID


class UpdateUserRequest(CreateUserRequest):
    role: str


class UpdatePasswordRequest(BaseModel):
    email: str


class UserResponse(BaseModel):
    id: uuid.UUID
    company_id: uuid.UUID | None
    email: str
    first_name: str | None = None
    last_name: str | None = None
    avatar_url: str | None = None
    role: str
    is_active: bool
    created_at: datetime
