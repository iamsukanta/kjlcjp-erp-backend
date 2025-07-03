import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import asyncio
from app.core.database import get_async_session
from app.models.user import Role, Permission, User
from sqlalchemy.future import select
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_roles_permissions():
    async with get_async_session() as session:
        # Check if roles already exist
        result = await session.execute(select(Role))
        existing_roles = result.scalars().all()
        if existing_roles:
            print("Roles and permissions already seeded.")
            return

        # Create permissions
        permission_names = [
            "create_user", "read_user", "update_user", "delete_user",
            "create_role", "read_role", "update_role", "delete_role",
            "create_company", "read_company", "update_company", "delete_company"
        ]
        permissions = [
            Permission(name=name)
            for name in permission_names
        ]

        # Create roles
        admin_role = Role(name="admin", permissions=permissions)
        user_role = Role(name="user")  # No permissions yet

        session.add_all(permissions + [admin_role, user_role])
        await session.commit()
        print("Seeded roles and permissions successfully.")

async def seed_admin_user():
    async with get_async_session() as session:
        result = await session.execute(select(User).where(User.email == "admin@example.com"))
        existing_admin = result.scalar_one_or_none()
        if existing_admin:
            print("Admin user already exists.")
            return

        # Fetch admin role
        result = await session.execute(select(Role).where(Role.name == "admin"))
        admin_role = result.scalar_one()

        admin_user = User(
            name="Admin User",
            email="admin@example.com",
            password=pwd_context.hash("admin123"),  # Hash password
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
