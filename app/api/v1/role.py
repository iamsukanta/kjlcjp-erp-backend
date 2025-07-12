from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import RoleOut, RoleCreate, PermissionCreate
from app.crud.role import create_role, update_role, get_all_roles, delete_role, create_permission
from app.core.database import get_async_session

router = APIRouter()

@router.post("/", response_model=RoleOut)
async def create_role(data: RoleCreate, db: AsyncSession = Depends(get_async_session)):
    return await create_role(db, data)

@router.put("/{role_id}", response_model=RoleOut)
async def update_role( role_id: int, data: RoleCreate, db: AsyncSession = Depends(get_async_session)):
    return await update_role(db, role_id, data)

@router.get("/", response_model=List[RoleOut])
async def all_roles(db: AsyncSession = Depends(get_async_session)):
    return await get_all_roles(db)

@router.delete("/{role_id}")
async def delete_role(role_id: int, db: AsyncSession = Depends(get_async_session)):
    return await delete_role(db, role_id)

