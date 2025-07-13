from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User, Role
from app.core.security import get_password_hash
from sqlalchemy.orm import selectinload


async def create_user(db: AsyncSession, userInfo: UserCreate, role_ids = []):
    print(role_ids , 'role ids ....')
    new_user = User(**userInfo.dict())
    if role_ids:
        roles_result = await db.execute(select(Role).where(Role.id.in_(role_ids)))
        new_user.roles = roles_result.scalars().all()
    else:
        new_user.roles = []
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return await get_user_by_email(db, userInfo.email)

async def update_user(db: AsyncSession, user_id: int, userInfo: UserUpdate, role_ids = []):
    result = await db.execute(
        select(User).options(selectinload(User.roles)).where(User.id == user_id)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in userInfo.dict(exclude_unset=True).items():
        setattr(user, key, value)

    if role_ids:
        roles_result = await db.execute(select(Role).where(Role.id.in_(role_ids)))
        user.roles = roles_result.scalars().all()

    await db.commit()
    await db.refresh(user)
    return await get_user_by_email(db, userInfo.email)

async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User).options(selectinload(User.roles).selectinload(Role.permissions)))
    return result.scalars().all()

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(User)
        .options(
            selectinload(User.roles).selectinload(Role.permissions)
        )
        .where(User.email == email)
    )
    return result.scalar_one_or_none()

async def get_user_details(db: AsyncSession, user_id: int):
    return await db.get(User, user_id)

async def delete_user(db: AsyncSession, user_id: int):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return {"detail": "Deleted successfully"}


