from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate

async def create_company(db: AsyncSession, company: CompanyCreate):
    new_company = Company(**company.dict())
    db.add(new_company)
    await db.commit()
    await db.refresh(new_company)
    return new_company

async def update_company(db: AsyncSession, company_id: int, company_data: CompanyUpdate):
    company = await db.get(Company, company_id)
    if not company:
        return None
    for key, value in company_data.dict(exclude_unset=True).items():
        setattr(company, key, value)
    await db.commit()
    await db.refresh(company)
    return company

async def get_companies(db: AsyncSession):
    result = await db.execute(select(Company))
    return result.scalars().all()
