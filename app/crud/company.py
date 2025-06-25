from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.company import Company
from app.schemas.company import CompanyCreate

async def create_company(db: AsyncSession, company: CompanyCreate):
    new_company = Company(**company.dict())
    db.add(new_company)
    await db.commit()
    await db.refresh(new_company)
    return new_company

async def get_companies(db: AsyncSession):
    result = await db.execute(select(Company))
    return result.scalars().all()
