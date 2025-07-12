from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserOut
from app.crud.user import create_user, get_all_users, get_user_details, delete_user
from app.core.database import get_async_session
import shutil, random, os

router = APIRouter()

UPLOAD_DIR = "uploads/users/profiles"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model= UserOut)
async def create_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role_ids: Optional[List[int]] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_async_session)
):
    try:
        file_path = None

        if file:
            random_prefix = str(random.randint(100000, 999999))
            file_location = f"{UPLOAD_DIR}/{random_prefix}_{file.filename}"
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file_path = file_location
        
        new_user = UserCreate(
            name=name,
            email=email,
            password=password
        )
        return await create_user(db, new_user, role_ids, file_path);
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{user_id}", response_model= UserOut)
async def update_user(user_id: int, data: UserCreate,  db: AsyncSession = Depends(get_async_session)):
    try:
        file_path = None
        if data.file:
            random_prefix = str(random.randint(100000, 999999))
            file_location = f"{UPLOAD_DIR}/{random_prefix}_{data.file.filename}"
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(data.file.file, buffer)
            file_path = file_location
        return await update_user(db, user_id, data, file_path);
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/", response_model=List[UserOut])
async def all_users(db: AsyncSession = Depends(get_async_session)):
    return await get_all_users(db)

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    return await get_user_details(db, user_id)

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    return await delete_user(db, user_id)
