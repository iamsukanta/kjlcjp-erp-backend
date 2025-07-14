from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User, Permission
from sqlalchemy.orm import selectinload


async def get_dashboard_statistics(db: AsyncSession):
    result = await db.execute(select(Permission))
    return result.scalars().all()


