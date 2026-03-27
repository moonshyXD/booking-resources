import uuid
from typing import Dict, Any

from catalog.domain.models.resource import Resource, ResourceRepositoryI
from catalog.repository.models.resource_status import ResourceStatus


class ResourceService:
    def __init__(self, repository: ResourceRepositoryI):
        self.repository = repository

    async def create_resource(self, resource: Resource) -> Resource:
        return await self.repository.create_resource(resource)

    async def get_resource(self, resource_id: uuid.UUID) -> Resource | None:
        return await self.repository.get_resource(resource_id)

    async def get_resources_by_company(self, company_id: uuid.UUID, skip: int, limit: int) -> list[Resource]:
        return await self.repository.get_resources_by_company(company_id, skip, limit)

    async def update_resource(self, resource_id: uuid.UUID, resource_data: Dict[str, Any]) -> Resource | None:
        return await self.repository.update_resource(resource_id, resource_data)

    async def update_resource_status(self, resource_id: uuid.UUID, status: ResourceStatus) -> Resource | None:
        return await self.repository.update_resource_status(resource_id, status)

    async def delete_resource(self, resource_id: uuid.UUID) -> bool:
        return await self.repository.delete_resource(resource_id)
