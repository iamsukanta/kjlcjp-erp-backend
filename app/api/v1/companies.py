from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import SessionLocal
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyRead
from app.crud import company as crud

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/", response_model=CompanyRead)
async def create(company: CompanyCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_company(db, company)

@router.put("/{company_id}", response_model=CompanyRead)
async def update(company_id: int, company: CompanyUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.update_company(db, company_id, company)

@router.get("/", response_model=list[CompanyRead])
async def read_all(db: AsyncSession = Depends(get_db)):
    return await crud.get_companies(db)
