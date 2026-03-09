from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func


class CompanyDB(DeclarativeBase):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
