from repository.models.base import Base
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    String,
    UniqueConstraint,
    UUID
)
from sqlalchemy.sql import func
from domain.models.user_role import UserRole
import uuid


class UserDB(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(
        UUID, nullable=False
    )
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    role = Column(String, default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("company_id", "email", name="unique_company_email"),
    )
