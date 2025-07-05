from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User, Role, Permission
from app.core.security import get_password_hash
from sqlalchemy.orm import selectinload

async def create_permission(db: AsyncSession, name: str):
    permission = Permission(name=name)
    db.add(permission)
    await db.commit()
    return permission

async def create_role(db: AsyncSession, name: str, permission_ids: list[str]):
    role = Role(name=name)
    role.permissions = await db.execute(select(Permission).where(Permission.id.in_(permission_ids)))
    role.permissions = role.permissions.scalars().all()
    db.add(role)
    await db.commit()
    return role

async def create_user(db: AsyncSession, name: str, email: str, password: str, role_ids: list[str]):
    hashed = get_password_hash(password)
    user = User(name=name, email=email, password=hashed)
    user.roles = await db.execute(select(Role).where(Role.id.in_(role_ids)))
    user.roles = user.roles.scalars().all()
    db.add(user)
    await db.commit()
    return user

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(User)
        .options(
            selectinload(User.roles).selectinload(Role.permissions)
        )
        .where(User.email == email)
    )
    return result.scalar_one_or_none()
