from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class CostBase(BaseModel):
    title: str
    voucher: Optional[str] = None
    amount: int
    entry_name: Optional[str] = None
    cost_type: Optional[str] = None
    cost_date: Optional[datetime] = None
    note: Optional[str] = None

class CostCreate(CostBase):
    pass

class CostUpdate(CostBase):
    pass

class CostRead(CostBase):
    id: int
    cost_document: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    created_by: Optional[int]
    updated_by: Optional[int]

    class Config:
        orm_mode = True
