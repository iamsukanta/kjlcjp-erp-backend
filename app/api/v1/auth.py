from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_session
from app.schemas.token import Token
from pydantic import BaseModel
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_refresh_token
from app.crud.user import get_user_by_email

class RefreshTokenRequest(BaseModel):
    refresh_token: str

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_async_session)):
    user = await get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = create_access_token(data={"id": user.id, "email": user.email})
    refresh_token = create_refresh_token(data={"id": user.id, "email": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
@router.post("/refresh", response_model=Token)
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
        return {
            "access_token": new_access_token,
            "refresh_token": req.refresh_token,
            "token_type": "bearer"
        }

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")