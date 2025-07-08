from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.income import Income
from app.schemas.income import IncomeCreate, IncomeUpdate
from sqlalchemy.exc import SQLAlchemyError

async def create_income(db: AsyncSession, income: IncomeCreate, file_path: str = None):
    new_income = Income(**income.dict(), income_document=file_path)
    db.add(new_income)
    await db.commit()
    await db.refresh(new_income)
    return new_income

async def get_incomes(db: AsyncSession):
    result = await db.execute(select(Income))
    return result.scalars().all()

async def get_income(db: AsyncSession, income_id: int):
    return await db.get(Income, income_id)

async def update_income(db: AsyncSession, income_id: int, income_data: IncomeUpdate, file_path: str = None):
    income = await db.get(Income, income_id)
    if not income:
        raise HTTPException(status_code=404, detail="Income not found")

    for key, value in income_data.dict(exclude_unset=True).items():
        setattr(income, key, value)

    if file_path:
        income.income_document = file_path

    await db.commit()
    await db.refresh(income)
    return income

async def delete_income(db: AsyncSession, income_id: int):
    income = await db.get(Income, income_id)
    if not income:
        raise HTTPException(status_code=404, detail="Income not found")
    await db.delete(income)
    await db.commit()
    return {"detail": "Deleted successfully"}
