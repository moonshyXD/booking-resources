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
    def get_company(self, company: Company): ...
    def add_company(self, company: Company): ...
    def delete_company(self, company: Company): ...
    def update_company(self, company: Company, new_company: Company): ...
