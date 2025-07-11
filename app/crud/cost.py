from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, and_
from fastapi import HTTPException
from typing import Optional, List, Tuple
from datetime import datetime, timedelta
from app.models.cost import Cost
from sqlalchemy.types import Date
from sqlalchemy.sql.expression import cast
from app.schemas.cost import CostCreate, CostUpdate
import logging
logger = logging.getLogger(__name__)

async def create_cost(db: AsyncSession, cost_data: CostCreate, file_path: str = None, user_id: int = None):
    new_cost = Cost(**cost_data.dict(), cost_document=file_path, created_by=user_id)
    db.add(new_cost)
    await db.commit()
    await db.refresh(new_cost)
    return new_cost

async def get_costs(
    db: AsyncSession,
    costType: Optional[str] = None,
    dateRange: Optional[str] = None,
    customFrom: Optional[str] = None,
    customTo: Optional[str] = None,
    titleSearch: Optional[str] = None,
    page: int = 1,
    limit: int = 10
) -> Tuple[List[Cost], int]:
    try:
        filters = []
        today = datetime.utcnow().date()

        if costType:
            filters.append(Cost.cost_type == costType)

        if titleSearch:
            filters.append(Cost.title.ilike(f"%{titleSearch}%"))

        if dateRange == "today":
            filters.append(cast(Cost.created_at, Date) == today)

        elif dateRange == "week":
            start = today - timedelta(days=today.weekday())
            end = start + timedelta(days=6)
            filters.append(and_(cast(Cost.created_at, Date) >= start,
                                cast(Cost.created_at, Date) <= end))

        elif dateRange == "month":
            start = today.replace(day=1)
            end = (start.replace(month=start.month % 12 + 1, day=1) - timedelta(days=1)) \
                if start.month != 12 else start.replace(year=start.year + 1, month=1, day=1) - timedelta(days=1)
            filters.append(and_(cast(Cost.created_at, Date) >= start,
                                cast(Cost.created_at, Date) <= end))

        elif dateRange == "custom" and customFrom and customTo:
            try:
                from_date = datetime.strptime(customFrom, "%Y-%m-%d").date()
                to_date = datetime.strptime(customTo, "%Y-%m-%d").date()
                filters.append(and_(cast(Cost.created_at, Date) >= from_date,
                                    cast(Cost.created_at, Date) <= to_date))
            except ValueError:
                raise ValueError("Invalid date format for customFrom or customTo. Use YYYY-MM-DD.")
        
        # Total count
        total_query = select(func.count()).select_from(Cost).where(*filters)
        total_result = await db.execute(total_query)
        total = total_result.scalar_one()

        # Pagination
        offset = (page - 1) * limit
        query = select(Cost).where(*filters).order_by(Cost.created_at.desc()).offset(offset).limit(limit)
        result = await db.execute(query)
        costs = result.scalars().all()
        return costs, total
    
    except Exception as e:
        logger.exception("Error while fetching costs.")
        raise RuntimeError("An error occurred while fetching costs.") from e

async def get_cost(db: AsyncSession, cost_id: int):
    return await db.get(Cost, cost_id)

async def update_cost(db: AsyncSession, cost_id: int, cost_data: CostUpdate, file_path: str = None, user_id: int = None):
    cost = await db.get(Cost, cost_id)
    if not cost:
        raise HTTPException(status_code=404, detail="Cost not found")
    for key, value in cost_data.dict(exclude_unset=True).items():
        setattr(cost, key, value)
    if file_path:
        cost.cost_document = file_path
    cost.updated_by = user_id
    await db.commit()
    await db.refresh(cost)
    return cost

async def delete_cost(db: AsyncSession, cost_id: int):
    cost = await db.get(Cost, cost_id)
    if not cost:
        raise HTTPException(status_code=404, detail="Cost not found")
    await db.delete(cost)
    await db.commit()
