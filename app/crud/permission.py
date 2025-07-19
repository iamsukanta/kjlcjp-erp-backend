from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.schemas.user import PermissionCreate
from app.models.user import User, Permission
from sqlalchemy.orm import selectinload

async def create_permission(db: AsyncSession, permissionInfo: PermissionCreate):
    result = await db.execute(
        select(Permission).where(func.lower(Permission.name) == permissionInfo.name.lower())
    )
    permission = result.scalars().first()
    if permission:
        raise HTTPException(status_code=404, detail="Permission already exists.");
    permission = Permission(name=permissionInfo.name)
    db.add(permission)
    await db.commit()
    return await get_permission(db, permission.id)

async def update_permission(db: AsyncSession, permission_id: int, permissionInfo: PermissionCreate):
    result = await db.execute(
        select(Permission).where(Permission.id == permission_id)
    )
    permission = result.scalars().first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    permission.name = permissionInfo.name 
    await db.commit()
    await db.refresh(permission)
    return await get_permission(db, permission.id)

async def get_permission(db: AsyncSession, permisson_id: int):
    result = await db.execute(
        select(Permission)
        .where(Permission.id == permisson_id)
    )
    return result.scalar_one_or_none()

async def get_all_permissions(db: AsyncSession):
    result = await db.execute(select(Permission))
    return result.scalars().all()

async def delete_permission(db: AsyncSession, permission_id: int):
    permission = await db.get(Permission, permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    await db.delete(permission)
    await db.commit()
    return {"detail": "Deleted successfully"}


