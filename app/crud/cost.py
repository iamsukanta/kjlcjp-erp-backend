from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.cost import Cost
from app.schemas.cost import CostCreate, CostUpdate

async def create_cost(db: AsyncSession, cost_data: CostCreate, file_path: str = None, user_id: int = None):
    new_cost = Cost(**cost_data.dict(), file=file_path, created_by=user_id)
    db.add(new_cost)
    await db.commit()
    await db.refresh(new_cost)
    return new_cost

async def get_costs(db: AsyncSession):
    result = await db.execute(select(Cost))
    return result.scalars().all()

async def get_cost(db: AsyncSession, cost_id: int):
    return await db.get(Cost, cost_id)

async def update_cost(db: AsyncSession, cost_id: int, cost_data: CostUpdate, file_path: str = None, user_id: int = None):
    cost = await db.get(Cost, cost_id)
    if not cost:
        raise HTTPException(status_code=404, detail="Cost not found")
    for key, value in cost_data.dict(exclude_unset=True).items():
        setattr(cost, key, value)
    if file_path:
        cost.file = file_path
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
