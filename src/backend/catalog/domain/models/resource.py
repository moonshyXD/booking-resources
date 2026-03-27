from __future__ import annotations
from uuid import UUID
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from catalog.repository.models.resource_status import ResourceStatus


@dataclass
class ResourceCategory:
    name: str
    id: UUID | None = None


@dataclass
class Resource:
    company_id: UUID
    category_id: UUID
    name: str
    status: ResourceStatus

    id: UUID | None = None
    info: str | None = None
    photo_url: str | None = None
    created_at: datetime | None = None


class ResourceRepositoryI(Protocol):
    async def create_resource(self, resource: Resource) -> Resource: ...
    async def get_resource(self, resource_id: UUID) -> Resource | None: ...
    async def get_resources_by_company(self, company_id: UUID, skip: int, limit: int) -> list[Resource]: ...
    async def update_resource(self, resource_id: UUID, resource: Resource) -> Resource | None: ...
    async def update_resource_status(self, resource_id: UUID, status: ResourceStatus) -> Resource | None: ...
    async def delete_resource(self, resource_id: UUID) -> bool: ...
