from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass
class Company:
    id: int
    name: str
    slug: str
    is_active: bool
    created_at: datetime


class CompanyRepositoryI(Protocol):
    async def get_company_by_id(self, company_id: int): ...
    async def add_company(self, company: Company): ...
    async def delete_company_by_id(self, company_id: int): ...
    async def update_company_by_id(self, company_id: int, new_company: Company): ...
