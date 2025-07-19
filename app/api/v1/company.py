from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_session
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyRead
from app.crud import company as crud
from app.core.permissions import has_permission

router = APIRouter()

@router.post("/", response_model=CompanyRead)
async def create(company: CompanyCreate, db: AsyncSession = Depends(get_async_session), _: bool = Depends(has_permission("create_company"))):
    return await crud.create_company(db, company)

@router.put("/{company_id}", response_model=CompanyRead)
async def update(company_id: int, company: CompanyUpdate, db: AsyncSession = Depends(get_async_session), _: bool = Depends(has_permission("update_company"))):
    return await crud.update_company(db, company_id, company)

@router.get("/", response_model=list[CompanyRead])
async def read_all(db: AsyncSession = Depends(get_async_session), _: bool = Depends(has_permission("read_company"))):
    return await crud.get_companies(db)