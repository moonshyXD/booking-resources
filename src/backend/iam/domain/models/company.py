from dataclasses import dataclass
from datetime import time
from typing import Protocol


@dataclass
class Company:
    id: int
    name: str
    slug: str
    is_active: bool
    created_at: time


class CompanyRepositoryI(Protocol):
    def get_company_by_id(self, company_id: int): ...
    def add_company(self, company: Company): ...
    def delete_company_by_id(self, company_id: int): ...
    def update_company_by_id(self, company_id: int, new_company: Company): ...
