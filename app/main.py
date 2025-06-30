from fastapi import FastAPI
from app.api.v1 import company, user, auth
from app.core.database import Base, engine

app = FastAPI()

app.include_router(company.router, prefix="/api/v1/companies", tags=["Companies"])
app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])

# Optional: create tables at startup (not for production)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
