from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.crud.user import create_user, update_user, get_all_users, get_user_details, delete_user
from app.core.database import get_async_session
import shutil, random, os
from app.core.security import get_password_hash
from app.core.permissions import has_permission

router = APIRouter()

UPLOAD_DIR = "uploads/users/profiles"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=UserOut)
async def add_new_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role_ids: Optional[List[int]] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_async_session),
    _: bool = Depends(has_permission("create_user"))
):
    try:
        file_path = None
        if file is not None:
            random_prefix = str(random.randint(100000, 999999))
            file_location = f"{UPLOAD_DIR}/{random_prefix}_{file.filename}"
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file_path = file_location
        hashed = get_password_hash(password)
        new_user = UserCreate(
            name=name,
            email=email,
            password=hashed,
            profile_image=file_path
        )
        return await create_user(db, userInfo=new_user, role_ids = role_ids);
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/{user_id}", response_model=UserOut)
async def edit_user(
    user_id: int,
    name: str = Form(...),
    email: str = Form(...),
    password: Optional[str] = Form(None),
    role_ids: Optional[List[int]] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_async_session),
    _: bool = Depends(has_permission("update_user"))
):
    try:
        file_path = None
        if file is not None:
            random_prefix = str(random.randint(100000, 999999))
            file_location = f"{UPLOAD_DIR}/{random_prefix}_{file.filename}"
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file_path = file_location

        updateUser = UserUpdate(
            name=name,
            email=email,
            profile_image=file_path
        )
        if password is not None: 
            hashed = get_password_hash(password)
            updateUser = UserUpdate(
                name=name,
                email=email,
                password=hashed,
                profile_image=file_path
            )
        return await update_user(db, user_id = user_id, userInfo=updateUser, role_ids = role_ids);
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[UserOut])
async def all_users(db: AsyncSession = Depends(get_async_session), _: bool = Depends(has_permission("read_user"))):
    return await get_all_users(db)

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_async_session), _: bool = Depends(has_permission("details_user"))):
    return await get_user_details(db, user_id)

@router.delete("/{user_id}")
async def remove_user(user_id: int, db: AsyncSession = Depends(get_async_session), _: bool = Depends(has_permission("delete_user"))):
    return await delete_user(db, user_id)
