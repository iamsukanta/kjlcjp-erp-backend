from pydantic import BaseModel

class CompanyCreate(BaseModel):
    name: str
    type: str

class CompanyRead(CompanyCreate):
    id: int

    class Config:
        orm_mode = True
