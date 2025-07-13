from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import PermissionOut, PermissionCreate
from app.crud.permission import get_all_permissions, update_permission, delete_permission, create_permission
from app.core.database import get_async_session

router = APIRouter()

@router.post("/")
async def add_permission(data: PermissionCreate, db: AsyncSession = Depends(get_async_session)):
    return await create_permission(db, data)

@router.put("/{role_id}", response_model=PermissionOut)
async def edit_permission( role_id: int, data: PermissionCreate, db: AsyncSession = Depends(get_async_session)):
    return await update_permission(db, role_id, data)

@router.get("/", response_model=List[PermissionOut])
async def all_permissions(db: AsyncSession = Depends(get_async_session)):
    return await get_all_permissions(db)

@router.delete("/{role_id}")
async def remove_permission(role_id: int, db: AsyncSession = Depends(get_async_session)):
    return await delete_permission(db, role_id)
