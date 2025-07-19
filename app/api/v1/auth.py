from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_session
from app.models.user import User, Role
from app.schemas.token import Token, ResponseLoginCredentials
from pydantic import BaseModel
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_refresh_token
from app.crud.user import get_user_by_email
from app.core.dependencies import get_current_user
from app.schemas.user import UserOut

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class LoginRequest(BaseModel):
    email: str
    password: str

router = APIRouter()

@router.get("/me")
async def get_current_user_info(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(User).options(selectinload(User.roles).selectinload(Role.permissions)).where(User.id == current_user.id)
    )
    return result.scalars().first()

@router.post("/login")
async def login(req: LoginRequest, db: AsyncSession = Depends(get_async_session)):
    user = await get_user_by_email(db, req.email)
    if not user or not verify_password(req.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = create_access_token(data={"id": user.id, "email": user.email})
    refresh_token = create_refresh_token(data={"id": user.id, "email": user.email})
    token_credentials = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
    return { "credentials": token_credentials, "user": user }
   
@router.post("/refresh")
async def refresh_token(req: RefreshTokenRequest, db: AsyncSession = Depends(get_async_session)):
    try:
        payload = decode_refresh_token(req.refresh_token)
        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        email: str = payload.get("email")
        user = await get_user_by_email(db, email=email)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        new_access_token = create_access_token(data={"id": user.id, "email": user.email})
        new_refresh_token = create_refresh_token(data={"id": user.id, "email": user.email})
        token_credentials = {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
        return { "credentials": token_credentials, "user": user }

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")