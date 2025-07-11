from fastapi import APIRouter, UploadFile, File, Query, Depends, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.cost import CostCreate, CostUpdate, CostRead, CostsResponseWithPagination
from app.crud.cost import create_cost, get_costs, update_cost, delete_cost, get_cost
from app.core.database import get_async_session
import shutil
import random
import os
from typing import List, Optional
from app.crud import cost as crud


router = APIRouter()

UPLOAD_DIR = "uploads/costs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=CostRead)
async def create_cost_entry(
    title: str = Form(...),
    amount: int = Form(...),
    voucher: str = Form(None),
    entry_name: str = Form(None),
    cost_type: str = Form(None),
    cost_date: str = Form(None),
    note: str = Form(None),
    file: UploadFile = File(None),
    db: AsyncSession = Depends(get_async_session),
    created_by: int = 1  # Replace with actual user extraction
):
    file_path = None
    if file:
        random_prefix = str(random.randint(100000, 999999))
        file_location = f"{UPLOAD_DIR}/{random_prefix}_{file.filename}"
        file_path = file_location
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    cost_data = CostCreate(
        title=title,
        amount=amount,
        voucher=voucher,
        entry_name=entry_name,
        cost_type=cost_type,
        cost_date=cost_date,
        note=note
    )
    return await create_cost(db, cost_data, file_path=file_path, user_id=created_by)

@router.get("/", response_model=CostsResponseWithPagination)
async def read_costs(
    cost_type: Optional[str] = Query(None),
    date_range: Optional[str] = Query(None),
    from_date: Optional[str] = Query(None),
    to_date: Optional[str] = Query(None),
    title: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_async_session)
):
    try:
        costs, total =  await crud.get_costs(
            db,
            costType=cost_type,
            dateRange=date_range,
            customFrom=from_date,
            customTo=to_date,
            titleSearch=title,
            page=page,
            limit=limit
        );

        return {
            "items": costs,
            "total": total,
            "page": page,
            "limit": limit
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{cost_id}", response_model=CostRead)
async def get_cost_entry(cost_id: int, db: AsyncSession = Depends(get_async_session)):
    cost = await get_cost(db, cost_id)
    if not cost:
        raise HTTPException(status_code=404, detail="Cost not found")
    return cost

@router.put("/{cost_id}", response_model=CostRead)
async def update_cost_entry(
    cost_id: int,
    title: str = Form(...),
    amount: int = Form(...),
    voucher: str = Form(None),
    entry_name: str = Form(None),
    cost_type: str = Form(None),
    cost_date: str = Form(None),
    note: str = Form(None),
    file: UploadFile = File(None),
    db: AsyncSession = Depends(get_async_session),
    updated_by: int = 1  # Replace with actual user
):
    file_path = None
    if file:
        random_prefix = str(random.randint(100000, 999999))
        file_location = f"{UPLOAD_DIR}/{random_prefix}_{file.filename}"
        file_path = file_location
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    cost_data = CostUpdate(
        title=title,
        amount=amount,
        voucher=voucher,
        entry_name=entry_name,
        cost_type=cost_type,
        cost_date=cost_date,
        note=note
    )
    return await update_cost(db, cost_id, cost_data, file_path=file_path, user_id=updated_by)

@router.delete("/{cost_id}")
async def delete_cost_entry(cost_id: int, db: AsyncSession = Depends(get_async_session)):
    await delete_cost(db, cost_id)
    return {"detail": "Deleted successfully"}
