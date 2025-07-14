from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.dashboard import get_dashboard_statistics
from app.core.database import get_async_session

router = APIRouter()
@router.get("/")
async def dashboard_statistics(db: AsyncSession = Depends(get_async_session)):
    return await get_dashboard_statistics(db)

