from domain.models.company import CompanyRepositoryI, Company


class CompanyService:
    def __init__(self, repository: CompanyRepositoryI):
        self.repository = repository

    async def add_company(self, company: Company):
        request = await self.repository.add_company(company)
        if request is None:
            return None

        return request

    async def delete_company(self, company_id: int):
        request = await self.repository.delete_company_by_id(company_id)
        if request is None:
            return None

        return request

    async def update_company(self, company_id: int, new_company: Company):
        request = await self.repository.update_company_by_id(company_id, new_company)
        if request is None:
            return None

        return request

    async def get_companies(self, offset: int = 0, limit: int = 20):
        return await self.repository.get_companies(offset=offset, limit=limit)