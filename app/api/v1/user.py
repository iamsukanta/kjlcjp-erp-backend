from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, RoleCreate, PermissionCreate
from app.crud.user import create_user, create_role, create_permission
from app.core.database import get_async_session

router = APIRouter()

@router.post("/")
async def register_user(data: UserCreate, db: AsyncSession = Depends(get_async_session)):
    return await create_user(db, data.name, data.email, data.password, data.role_ids)

@router.post("/roles")
async def add_role(data: RoleCreate, db: AsyncSession = Depends(get_async_session)):
    return await create_role(db, data.name, data.permission_ids)

@router.post("/permissions")
async def add_permission(data: PermissionCreate, db: AsyncSession = Depends(get_async_session)):
    return await create_permission(db, data.name)
