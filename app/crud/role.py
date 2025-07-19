from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.schemas.user import RoleCreate
from app.models.user import Role, Permission
from sqlalchemy.orm import selectinload

async def create_role(db: AsyncSession, roleInfo: RoleCreate):
    result = await db.execute(
        select(Role).where(func.lower(Role.name) == roleInfo.name.lower())
    )
    role = result.scalars().first()
    if role:
        raise HTTPException(status_code=404, detail="Role already exists.");
    role = Role(name=roleInfo.name)
    if roleInfo.permission_ids:
        permission_result = await db.execute(select(Permission).where(Permission.id.in_(roleInfo.permission_ids)))
        role.permissions = permission_result.scalars().all()
    else:
        role.permissions = []
    db.add(role)
    await db.commit()
    return await get_role(db, role.id);

async def update_role(db: AsyncSession, role_id: int, roleInfo: RoleCreate):
    result = await db.execute(
        select(Role).options(selectinload(Role.permissions)).where(Role.id == role_id)
    )
    role = result.scalars().first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    role.name = roleInfo.name
    if roleInfo.permission_ids:
        permission_result = await db.execute(select(Permission).where(Permission.id.in_(roleInfo.permission_ids)))
        role.permissions = permission_result.scalars().all()
    else:
        role.permissions = []
    await db.commit()
    await db.refresh(role)
    return await get_role(db, role.id);

async def get_role(db: AsyncSession, role_id: int):
    result = await db.execute(
        select(Role)
        .options(
            selectinload(Role.permissions)
        )
        .where(Role.id == role_id)
    )
    return result.scalar_one_or_none()

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


