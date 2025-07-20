# seed.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import asyncio
from app.core.database import SessionLocal
from app.models.user import Role, Permission, User
from sqlalchemy import select
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_roles_permissions():
    async with SessionLocal() as session:
        result = await session.execute(select(Role))
        existing_roles = result.scalars().all()
        if existing_roles:
            print("Roles and permissions already seeded.")
            return

        permission_names = [
            "dashboard_statistics",
            "create_user", "read_user", "update_user", "delete_user", "details_user",
            "create_role", "read_role", "update_role", "delete_role", "details_role",
            "create_permission", "read_permission", "update_permission", "delete_permission", "details_permission",
            "create_income", "read_income", "update_income", "delete_income", "details_income",
            "create_cost", "read_cost", "update_cost", "delete_cost", "details_cost"
        ]
        permissions = [Permission(name=name) for name in permission_names]

        admin_role = Role(name="Admin", permissions=permissions)
        user_role = Role(name="Manager")  # no permissions

        session.add_all(permissions + [admin_role, user_role])
        await session.commit()
        print("Seeded roles and permissions successfully.")

async def seed_admin_user():
    async with SessionLocal() as session:
        result = await session.execute(select(User).where(User.email == "admin@kjlcjp.com"))
        existing_admin = result.scalar_one_or_none()
        if existing_admin:
            print("Admin user already exists.")
            return

        result = await session.execute(select(Role).where(Role.name == "Admin"))
        admin_role = result.scalar_one()

        admin_user = User(
            name="Admin User",
            email="admin@kjlcjp.com",
            password=pwd_context.hash("admin1234"),
            roles=[admin_role]
        )

        session.add(admin_user)
        await session.commit()
        print("Admin user created successfully.")

async def main():
    await seed_roles_permissions()
    await seed_admin_user()

if __name__ == "__main__":
    asyncio.run(main())
