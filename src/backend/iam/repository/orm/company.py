from dataclasses import asdict

from domain.models.company import Company
from repository.models.company import CompanyDB
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_


class CompanyRepositoryPostgres:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_company_by_id(self, company_id: int) -> Company | None:
        company_db = await self.session.get(CompanyDB, company_id)
        if company_db is None:
            return None

        return self.to_entity(company_db)

    async def get_company_by_slug(self, slug: str) -> Company | None:
        stmt = select(CompanyDB).where(CompanyDB.slug == slug)
        result = await self.session.execute(stmt)
        company_db = result.scalar_one_or_none()
        if company_db is None:
            return None

        return self.to_entity(company_db)

    async def add_company(self, company: Company) -> Company | None:
        company_data = self._validate_company_data(company)
        
        query = select(CompanyDB).where(
            or_(
                CompanyDB.name == company.name,
                CompanyDB.slug == company.slug
            )
        )
        result = await self.session.execute(query)
        existing_company = result.scalar_one_or_none()
        if existing_company is not None:
            return None
            
        company_db = CompanyDB(**company_data)
        self.session.add(company_db)
        await self.session.flush()
        return self.to_entity(company_db)

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
        return self.to_entity(company_db)

    async def delete_company_by_id(self, company_id: int) -> Company | None:
        company_db = await self.session.get(CompanyDB, company_id)
        if company_db is None:
            return None

        await self.session.delete(company_db)
        await self.session.flush()
        return self.to_entity(company_db)

    async def get_companies(self, offset: int = 0, limit: int = 20) -> list[Company]:
        stmt = select(CompanyDB).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        companies_db = result.scalars().all()
        return [self.to_entity(company) for company in companies_db]

    @staticmethod
    def _validate_company_data(company: Company) -> dict:
        data = asdict(company)
        data.pop("id", None)
        data.pop("created_at", None)
        return data

    @staticmethod
    def to_entity(company_db_instance: CompanyDB) -> Company:
        return Company(
            id=company_db_instance.id,
            name=company_db_instance.name,
            slug=company_db_instance.slug,
            is_active=company_db_instance.is_active,
            created_at=company_db_instance.created_at,
        )
