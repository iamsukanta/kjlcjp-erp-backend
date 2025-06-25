from fastapi import FastAPI
from app.api.v1 import companies
from app.core.database import Base, engine

app = FastAPI()

app.include_router(companies.router, prefix="/api/v1/companies", tags=["Companies"])

# Optional: create tables at startup (not for production)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
