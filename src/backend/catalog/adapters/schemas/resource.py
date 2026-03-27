import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from catalog.repository.models.resource_status import ResourceStatus


class Resource(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    company_id: uuid.UUID
    category_id: uuid.UUID
    name: str
    info: str | None = None
    photo_url: str | None = None
    status: ResourceStatus
    created_at: datetime


class CreateResourceRequest(BaseModel):
    company_id: uuid.UUID
    category_id: uuid.UUID
    name: str = Field(..., examples=["Meeting room A-101"])
    info: str | None = Field(None, examples=["Large room for up to 12 people"])
    photo_url: str | None = Field(None, examples=["https://example.com/resource.jpg"])
    status: ResourceStatus = Field(ResourceStatus.FREE, examples=["FREE"])


class UpdateResourceRequest(BaseModel):
    name: str | None = Field(None, examples=["Meeting room A-102"])
    info: str | None = Field(None, examples=["Updated room description"])
    photo_url: str | None = Field(None, examples=["https://example.com/new_resource.jpg"])
    status: ResourceStatus | None = Field(None, examples=["MAINTENANCE"])


class ResourceStatusUpdateRequest(BaseModel):
    status: ResourceStatus = Field(..., examples=["MAINTENANCE"])
