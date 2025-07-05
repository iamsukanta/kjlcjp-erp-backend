# dependencies/permissions.py
from fastapi import Depends, HTTPException, status
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user

def has_permission(permission_name: str):
    async def checker(
        current_user: User = Depends(get_current_user),
    ):
        # Check if the user has the permission through any of their roles
        for role in current_user.roles:
            for permission in role.permissions:
                if permission.name == permission_name:
                    return True
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing permission: {permission_name}"
        )
    return checker
