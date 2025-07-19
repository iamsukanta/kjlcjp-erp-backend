from pydantic import BaseModel

class UserOut(BaseModel):
    totalCompanyIncome: int = 0;
    totalCompanyCost: int = 0;
    totalCompanyProfit: int = 0;
    totalSchoolIncome: int = 0;
    totalSchoolCost: int = 0;
    totalSchoolProfit: int = 0;

    class Config:
        orm_mode = True
