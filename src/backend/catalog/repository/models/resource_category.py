import uuid

from sqlalchemy import Column, String, UUID, text
from sqlalchemy.orm import relationship

from catalog.repository.models.base import Base


class ResourceCategoryDB(Base):
    __tablename__ = "resource_categories"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    name = Column(String(100), unique=True, nullable=False)

    resources = relationship("ResourceDB", back_populates="category")
