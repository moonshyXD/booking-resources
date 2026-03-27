import uuid

from pydantic import BaseModel, ConfigDict, Field


class ResourceCategoryBase(BaseModel):
    name: str = Field(..., max_length=100, examples=["Meeting room"])


class ResourceCategoryCreate(ResourceCategoryBase):
    pass


class ResourceCategory(ResourceCategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
