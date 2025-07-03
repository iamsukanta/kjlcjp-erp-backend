from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings
from contextlib import asynccontextmanager

DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI.replace("postgresql+psycopg2", "postgresql+asyncpg")

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

@asynccontextmanager
async def get_async_session():
    async with SessionLocal() as session:
        yield session

class Base(DeclarativeBase):
    pass
