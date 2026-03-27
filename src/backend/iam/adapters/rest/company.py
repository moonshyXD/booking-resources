import uuid
from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException, Query

from iam.adapters.schemas.company import CompanyRequest, CompanyResponse
from iam.adapters.dependencies.company import get_company_service
from iam.adapters.dependencies.auth import require_admin
from iam.usecases.company import CompanyService
from iam.domain.models.company import Company

router = APIRouter(
    prefix="/companies",
    tags=["companies"]
)

@router.get(path="/v1", response_model=list[CompanyResponse])
async def get_companies(
    service: Annotated[CompanyService, Depends(get_company_service)],
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
) -> list[CompanyResponse]:
    return await service.get_companies(offset=offset, limit=limit)

@router.post(
    path="/v1",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)]
)
async def add_company(
        company: CompanyRequest,
        service: Annotated[CompanyService, Depends(get_company_service)]
) -> CompanyResponse:
    domain_company = Company(name=company.name, slug=company.slug, is_active=company.is_active)
    result = await service.add_company(domain_company)
    if result is None:
        raise HTTPException(
            status_code=409,
            detail="Ошибка создания компании. Заполните все поля и проверьте правильность ввёдённого названия, слага и статуса компании"
        )
    return result

@router.delete(
    path="/v1/{company_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)]
)
async def delete_company(
        company_id: uuid.UUID,
        service: Annotated[CompanyService, Depends(get_company_service)]
):
    result = await service.delete_company(company_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Компания не найдена")

@router.put(
    path="/v1/{company_id}",
    response_model=CompanyResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_admin)]
)
async def update_company(
        company_id: uuid.UUID,
        new_company: CompanyRequest,
        service: Annotated[CompanyService, Depends(get_company_service)]
) -> CompanyResponse:
    domain_company = Company(name=new_company.name, slug=new_company.slug, is_active=new_company.is_active)
    result = await service.update_company(company_id, domain_company)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Компания не найдена или вы попытались изменить название на существующую компанию"
        )

    return result