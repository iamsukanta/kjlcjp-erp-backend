from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class PermissionBase(BaseModel):
    name: str

class PermissionCreate(PermissionBase):
    pass

class PermissionOut(PermissionBase):
    id: int

    class Config:
        orm_mode = True

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    permission_ids: List[str]

class RoleOut(RoleBase):
    id: int
    permissions: List[PermissionOut]

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    email: EmailStr
    profile_image: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role_ids: List[str]

class UserOut(UserBase):
    id: int
    roles: List[RoleOut]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
