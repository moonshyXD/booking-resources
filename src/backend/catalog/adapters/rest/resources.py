import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from catalog.adapters.dependencies.resource import get_resource_service
from catalog.adapters.schemas.resource import (
    CreateResourceRequest,
    Resource as ResourceSchema,
    ResourceStatusUpdateRequest,
    UpdateResourceRequest,
)
from catalog.adapters.dependencies.auth import require_company_admin
from catalog.domain.models.resource import Resource as ResourceDomain
from catalog.usecases.resource import ResourceService

router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.get(path="/v1/{company_id}", response_model=list[ResourceSchema])
async def get_catalog_items(
    company_id: uuid.UUID,
    service: Annotated[ResourceService, Depends(get_resource_service)],
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
) -> list[ResourceDomain]:
    items = await service.get_resources_by_company(company_id, offset, limit)
    return items


@router.post(
    path="/v1",
    response_model=ResourceSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_company_admin)],
)
async def create_catalog_item(
    resource_data: CreateResourceRequest,
    service: Annotated[ResourceService, Depends(get_resource_service)],
) -> ResourceDomain:
    resource_domain = ResourceDomain(**resource_data.model_dump())
    created_item = await service.create_resource(resource_domain)
    return created_item


@router.put(
    path="/v1/{resource_id}",
    response_model=ResourceSchema,
    dependencies=[Depends(require_company_admin)],
)
async def update_catalog_item(
    resource_id: uuid.UUID,
    resource_data: UpdateResourceRequest,
    service: Annotated[ResourceService, Depends(get_resource_service)],
) -> ResourceDomain:
    updated_item = await service.update_resource(resource_id, resource_data.model_dump(exclude_unset=True))
    if not updated_item:
        raise HTTPException(status_code=404, detail="Resource not found")
    return updated_item


@router.patch(
    path="/v1/{resource_id}/status",
    response_model=ResourceSchema,
    dependencies=[Depends(require_company_admin)],
)
async def update_catalog_item_status(
    resource_id: uuid.UUID,
    status_data: ResourceStatusUpdateRequest,
    service: Annotated[ResourceService, Depends(get_resource_service)],
) -> ResourceDomain:
    updated_item = await service.update_resource_status(resource_id, status_data.status)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Resource not found")
    return updated_item


@router.delete(
    path="/v1/{resource_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_company_admin)],
)
async def delete_catalog_item(
    resource_id: uuid.UUID,
    service: Annotated[ResourceService, Depends(get_resource_service)],
):
    deleted = await service.delete_resource(resource_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Resource not found.")
