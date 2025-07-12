from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.user import RoleCreate
from app.models.user import User, Role, Permission
from sqlalchemy.orm import selectinload

async def create_permission(db: AsyncSession, name: str):
    permission = Permission(name=name)
    db.add(permission)
    await db.commit()
    return permission

async def create_role(db: AsyncSession, roleInfo: RoleCreate):
    role = Role(name=roleInfo.name)
    role.permissions = await db.execute(select(Permission).where(Permission.id.in_(roleInfo.permission_ids)))
    role.permissions = role.permissions.scalars().all()
    db.add(role)
    await db.commit()
    return role

async def update_role(db: AsyncSession, role_id: int, roleInfo: RoleCreate):
    role = await db.get(User, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    for key, value in roleInfo.dict(exclude_unset=True).items():
        setattr(role, key, value)
    
    role.permissions = await db.execute(select(Permission).where(Permission.id.in_(roleInfo.permission_ids)))
    role.permissions = role.permissions.scalars().all()

    await db.commit()
    await db.refresh(role)
    return role

async def get_all_roles(db: AsyncSession):
    result = await db.execute(select(Role).options(selectinload(Role.permissions)))
    return result.scalars().all()

async def delete_role(db: AsyncSession, role_id: int):
    role = await db.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    await db.delete(role)
    await db.commit()
    return {"detail": "Deleted successfully"}


