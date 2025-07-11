from pydantic import BaseModel
from typing import List
from typing import Optional
from datetime import datetime

class IncomeBase(BaseModel):
    title: str
    source: Optional[str] = None
    amount: int
    collection_sin: Optional[str] = None
    income_type: Optional[str] = None
    collection_date: Optional[datetime] = None
    note: Optional[str] = None

class IncomeCreate(IncomeBase):
    created_by: Optional[int]

class IncomeUpdate(IncomeBase):
    updated_by: Optional[int]

class IncomeRead(IncomeBase):
    id: int
    income_document: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    created_by: Optional[int]
    updated_by: Optional[int]

class IncomesResponseWithPagination(BaseModel):
    items: List[IncomeRead]
    total: int
    page: int
    limit: int

    class Config:
        orm_mode = True
