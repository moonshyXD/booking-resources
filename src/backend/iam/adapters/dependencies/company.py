from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from iam.usecases.company import CompanyService
from iam.repository.orm.company import CompanyRepositoryPostgres

from iam.adapters.dependencies.general import get_db_session

def get_company_service(session: Annotated[AsyncSession, Depends(get_db_session)]) -> CompanyService:
    return CompanyService(repository=CompanyRepositoryPostgres(session))