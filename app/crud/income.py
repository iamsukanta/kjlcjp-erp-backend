from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, and_
from fastapi import HTTPException
from typing import Optional, List, Tuple
from datetime import datetime, timedelta
from app.models.income import Income
from sqlalchemy.types import Date
from sqlalchemy.sql.expression import cast
from app.schemas.income import IncomeCreate, IncomeUpdate
import logging
logger = logging.getLogger(__name__)

async def create_income(db: AsyncSession, income: IncomeCreate, file_path: str = None):
    new_income = Income(**income.dict(), income_document=file_path)
    db.add(new_income)
    await db.commit()
    await db.refresh(new_income)
    return new_income

async def get_incomes(
    db: AsyncSession,
    incomeType: Optional[str] = None,
    dateRange: Optional[str] = None,
    customFrom: Optional[str] = None,
    customTo: Optional[str] = None,
    titleSearch: Optional[str] = None,
    page: int = 1,
    limit: int = 10
) -> Tuple[List[Income], int]:
    try:
        filters = []
        today = datetime.utcnow().date()

        if incomeType:
            filters.append(Income.income_type == incomeType)

        if titleSearch:
            filters.append(Income.title.ilike(f"%{titleSearch}%"))

        if dateRange == "today":
            filters.append(cast(Income.created_at, Date) == today)

        elif dateRange == "week":
            start = today - timedelta(days=today.weekday())
            end = start + timedelta(days=6)
            filters.append(and_(cast(Income.created_at, Date) >= start,
                                cast(Income.created_at, Date) <= end))

        elif dateRange == "month":
            start = today.replace(day=1)
            end = (start.replace(month=start.month % 12 + 1, day=1) - timedelta(days=1)) \
                if start.month != 12 else start.replace(year=start.year + 1, month=1, day=1) - timedelta(days=1)
            filters.append(and_(cast(Income.created_at, Date) >= start,
                                cast(Income.created_at, Date) <= end))

        elif dateRange == "custom" and customFrom and customTo:
            try:
                from_date = datetime.strptime(customFrom, "%Y-%m-%d").date()
                to_date = datetime.strptime(customTo, "%Y-%m-%d").date()
                filters.append(and_(cast(Income.created_at, Date) >= from_date,
                                    cast(Income.created_at, Date) <= to_date))
            except ValueError:
                raise ValueError("Invalid date format for customFrom or customTo. Use YYYY-MM-DD.")
        
        # Total count
        total_query = select(func.count()).select_from(Income).where(*filters)
        total_result = await db.execute(total_query)
        total = total_result.scalar_one()

        # Pagination
        offset = (page - 1) * limit
        query = select(Income).where(*filters).order_by(Income.created_at.desc()).offset(offset).limit(limit)
        result = await db.execute(query)
        incomes = result.scalars().all()
        return incomes, total
    
    except Exception as e:
        logger.exception("Error while fetching costs.")
        raise RuntimeError("An error occurred while fetching costs.") from e

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
