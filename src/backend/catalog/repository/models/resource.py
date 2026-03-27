import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text,
    UUID,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from catalog.repository.models.base import Base
from catalog.repository.models.resource_status import ResourceStatus


class ResourceDB(Base):
    __tablename__ = "resources"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    company_id = Column(UUID(as_uuid=True), nullable=False)
    category_id = Column(ForeignKey("resource_categories.id"), nullable=False)
    name = Column(String(255), nullable=False)
    info = Column(Text, nullable=True)
    photo_url = Column(String(255), nullable=True)
    status = Column(
        Enum(ResourceStatus),
        nullable=False,
        default=ResourceStatus.FREE,
        server_default=text("'FREE'"),
    )
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    category = relationship("ResourceCategoryDB", back_populates="resources")
