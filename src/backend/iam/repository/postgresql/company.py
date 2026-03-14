from dataclasses import asdict

from domain.models.company import Company
from repository.models.company import CompanyDB
from sqlalchemy.ext.asyncio import AsyncSession


class CompanyRepositoryPostgres:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_company_by_id(self, company_id: int) -> Company | None:
        company_db = await self.session.get(CompanyDB, company_id)
        if company_db is None:
            return None
        return self._to_entity(company_db)

    async def add_company(self, company: Company) -> Company:
        company_data = self._validate_company_data(company)
        company_db = CompanyDB(**company_data)
        self.session.add(company_db)
        await self.session.flush()
        return self._to_entity(company_db)

    async def update_company_by_id(
            self, company_id: int, new_company: Company
    ) -> Company | None:
        company_db = await self.session.get(CompanyDB, company_id)
        if company_db is None:
            return None

        new_company_data = self._validate_company_data(new_company)
        for key, value in new_company_data.items():
            setattr(company_db, key, value)

        await self.session.flush()
        return self._to_entity(company_db)

    async def delete_company_by_id(self, company_id: int) -> Company | None:
        company_db = await self.session.get(CompanyDB, company_id)
        if company_db is None:
            return None

        self.session.delete(company_db)
        await self.session.flush()
        return self._to_entity(company_db)

    @staticmethod
    def _validate_company_data(company: Company) -> dict:
        data = asdict(company)
        data.pop("id", None)
        data.pop("created_at", None)
        return data

    @staticmethod
    def _to_entity(company_db_instance: CompanyDB) -> Company:
        return Company(
            id=company_db_instance.id,
            name=company_db_instance.name,
            slug=company_db_instance.slug,
            is_active=company_db_instance.is_active,
            created_at=company_db_instance.created_at,
        )
