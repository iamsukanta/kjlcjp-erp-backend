from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.user import PermissionCreate
from app.models.user import User, Permission
from sqlalchemy.orm import selectinload

async def create_permission(db: AsyncSession, permissionInfo: PermissionCreate):
    permission = Permission(name=permissionInfo.name)
    db.add(permission)
    await db.commit()
    return permission

async def update_permission(db: AsyncSession, permission_id: int, permissionInfo: PermissionCreate):
    permission = await db.get(User, permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    for key, value in permissionInfo.dict(exclude_unset=True).items():
        setattr(permission, key, value)
    
    await db.commit()
    await db.refresh(permission)
    return permission

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


