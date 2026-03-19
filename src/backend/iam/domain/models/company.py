from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass
class Company:
    name: str
    slug: str
    
    id: int | None = None
    is_active: bool = True
    created_at: datetime | None = None


class CompanyRepositoryI(Protocol):
    async def get_company_by_id(self, company_id: int): ...
    async def add_company(self, company: Company): ...
    async def delete_company_by_id(self, company_id: int): ...
    async def update_company_by_id(self, company_id: int, new_company: Company): ...
    async def get_companies(self, offset: int = 0, limit: int = 20): ...
