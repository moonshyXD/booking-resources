import uuid
from typing import Dict, Any
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from catalog.domain.models.resource import Resource
from catalog.repository.models.resource import ResourceDB
from catalog.repository.models.resource_status import ResourceStatus


class ResourceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_resource(self, resource: Resource) -> Resource:
        new_resource_db = self.to_db_model(resource)
        self.session.add(new_resource_db)
        await self.session.flush()
        return self.to_entity(new_resource_db)

    async def get_resource(self, resource_id: uuid.UUID) -> Resource | None:
        resource_db = await self.session.get(ResourceDB, resource_id)
        if not resource_db:
            return None
        return self.to_entity(resource_db)

    async def get_resources_by_company(self, company_id: uuid.UUID, skip: int, limit: int) -> list[Resource]:
        result = await self.session.execute(
            select(ResourceDB)
            .where(ResourceDB.company_id == company_id)
            .offset(skip)
            .limit(limit)
        )
        resources_db = result.scalars().all()
        return [self.to_entity(res) for res in resources_db]

    async def update_resource(self, resource_id: uuid.UUID, resource_data: Dict[str, Any]) -> Resource | None:
        resource_data = {k: v for k, v in resource_data.items() if v is not None}
        if not resource_data:
            return await self.get_resource(resource_id)

        await self.session.execute(
            update(ResourceDB)
            .where(ResourceDB.id == resource_id)
            .values(**resource_data)
        )
        await self.session.flush()
        return await self.get_resource(resource_id)

    async def update_resource_status(self, resource_id: uuid.UUID, status: ResourceStatus) -> Resource | None:
        resource_db = await self.session.get(ResourceDB, resource_id)
        if not resource_db:
            return None
        
        resource_db.status = status
        await self.session.flush()
        return self.to_entity(resource_db)

    async def delete_resource(self, resource_id: uuid.UUID) -> bool:
        resource_db = await self.session.get(ResourceDB, resource_id)
        if not resource_db:
            return False
        await self.session.delete(resource_db)
        await self.session.flush()
        return True

    @staticmethod
    def to_entity(resource_db: ResourceDB) -> Resource:
        return Resource(
            id=resource_db.id,
            company_id=resource_db.company_id,
            category_id=resource_db.category_id,
            name=resource_db.name,
            info=resource_db.info,
            photo_url=resource_db.photo_url,
            status=resource_db.status,
            created_at=resource_db.created_at,
        )

    @staticmethod
    def to_db_model(resource: Resource) -> ResourceDB:
        return ResourceDB(
            id=resource.id,
            company_id=resource.company_id,
            category_id=resource.category_id,
            name=resource.name,
            info=resource.info,
            photo_url=resource.photo_url,
            status=resource.status,
        )
