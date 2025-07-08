from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import DateTime
from typing import List
import shutil
import random
import os
from app.schemas.income import IncomeCreate, IncomeUpdate, IncomeRead
from app.crud import income as crud
from app.core.database import get_async_session

router = APIRouter()

UPLOAD_DIR = "uploads/incomes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=IncomeRead)
async def create_income(
    title: str = Form(...),
    source: str = Form(...),
    amount: int = Form(...),
    collection_sin: str = Form(None),
    income_type: str = Form(None),
    collection_date: str = Form(None),
    note: str = Form(None),
    created_by: int = Form(None),
    file: UploadFile = File(None),
    db: AsyncSession = Depends(get_async_session)
):
    file_path = None
    if file:
        random_prefix = str(random.randint(100000, 999999))
        file_location = f"{UPLOAD_DIR}/{random_prefix}_{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_path = file_location

    income_data = IncomeCreate(
        title=title, source=source, amount=amount,
        collection_sin=collection_sin, income_type=income_type,
        collection_date=collection_date, note=note, created_by=created_by
    )

    return await crud.create_income(db, income=income_data, file_path=file_path)

@router.get("/", response_model=List[IncomeRead])
async def read_incomes(db: AsyncSession = Depends(get_async_session)):
    return await crud.get_incomes(db)

@router.get("/{income_id}", response_model=IncomeRead)
async def read_income(income_id: int, db: AsyncSession = Depends(get_async_session)):
    return await crud.get_income(db, income_id)

@router.put("/{income_id}", response_model=IncomeRead)
async def update_income(
    income_id: int,
    title: str = Form(...),
    source: str = Form(...),
    amount: int = Form(...),
    collection_sin: str = Form(None),
    income_type: str = Form(None),
    collection_date: str = Form(None),
    note: str = Form(None),
    updated_by: int = Form(None),
    file: UploadFile = File(None),
    db: AsyncSession = Depends(get_async_session)
):
    file_path = None
    if file:
        random_prefix = str(random.randint(100000, 999999))
        file_location = f"{UPLOAD_DIR}/{random_prefix}_{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_path = file_location

    income_data = IncomeUpdate(
        title=title, source=source, amount=amount,
        collection_sin=collection_sin, income_type=income_type,
        collection_date=collection_date, note=note, updated_by=updated_by
    )

    return await crud.update_income(db, income_id, income_data, file_path=file_path)

@router.delete("/{income_id}")
async def delete_income(income_id: int, db: AsyncSession = Depends(get_async_session)):
    return await crud.delete_income(db, income_id)
