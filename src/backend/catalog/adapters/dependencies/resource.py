from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from catalog.usecases.resource import ResourceService
from catalog.repository.orm.resource import ResourceRepository
from catalog.adapters.dependencies.general import get_db_session


def get_resource_service(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> ResourceService:
    return ResourceService(repository=ResourceRepository(session))
