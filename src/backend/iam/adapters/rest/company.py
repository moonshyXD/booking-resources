from fastapi import APIRouter, status, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from adapters.rest.database import get_db_session
from typing import Annotated
from usecases.company import CompanyService
from domain.models.company import Company
from repository.postgresql.company import CompanyRepositoryPostgres

router = APIRouter(prefix="/companies", tags=["companies"])

class CompanyRequest(BaseModel):
    name: str
    slug: str
    is_active: bool = True

class CompanyResponse(CompanyRequest):
    id: int
    created_at: datetime


def get_company_service(session: Annotated[AsyncSession, Depends(get_db_session)]) -> CompanyService:
    return CompanyService(repository=CompanyRepositoryPostgres(session))


@router.get(path="/v1", response_model=list[CompanyResponse], status_code=status.HTTP_200_OK)
async def get_companies(
    service: Annotated[CompanyService, Depends(get_company_service)],
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
) -> list[CompanyResponse]:
    return await service.get_companies(offset=offset, limit=limit)


@router.post(path="/v1", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def add_company(company: CompanyRequest,
                   service: Annotated[CompanyService, Depends(get_company_service)]
                   ) -> CompanyResponse:
    domain_company = Company(
        name=company.name,
        slug=company.slug,
        is_active=company.is_active
    )
    request = await service.add_company(domain_company)
    if request is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Компания уже есть в базе"
        )

    return request

@router.delete(path="/v1/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
        company_id: int,
        service: Annotated[CompanyService, Depends(get_company_service)]
    ):
    request = await service.delete_company(company_id)
    if request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Компания не найдена"
        )

@router.put(path="/v1/{company_id}", response_model=CompanyResponse, status_code=status.HTTP_200_OK)
async def update_company(
        company_id: int,
        new_company: CompanyRequest,
        service: Annotated[CompanyService, Depends(get_company_service)]
    ) -> CompanyResponse:
    domain_company = Company(
        name=new_company.name,
        slug=new_company.slug,
        is_active=new_company.is_active
    )
    request = await service.update_company(company_id, domain_company)
    if request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Компания не найдена"
        )

    return request
