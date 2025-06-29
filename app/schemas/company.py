from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class CompanyBase(BaseModel):
    name: str
    type: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None

class CompanyCreate(CompanyBase):
    created_by: Optional[int] = None

class CompanyUpdate(CompanyBase):
    updated_by: Optional[int] = None

class CompanyRead(CompanyBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    class Config:
        orm_mode = True

