from pydantic import BaseModel
import uuid
from datetime import datetime

class CompanyRequest(BaseModel):
    name: str
    slug: str
    is_active: bool = True

class CompanyResponse(CompanyRequest):
    id: uuid.UUID
    created_at: datetime
