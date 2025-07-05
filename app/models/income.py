from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Income(Base):
    __tablename__ = "incomes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    collection_sin: Mapped[str] = mapped_column(String(255), nullable=True) 
    collection_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    income_type: Mapped[str] = mapped_column(String(50), nullable=False)
    file: Mapped[str] = mapped_column(String(255), nullable=True)
    note: Mapped[Text] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
