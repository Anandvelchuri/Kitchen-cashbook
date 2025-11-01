from pydantic import BaseModel, Field
from typing import Optional


class EntryCreate(BaseModel):
    type: str = Field(..., description="'income' or 'expense'")
    amount: float
    category: Optional[str] = None
    date: str  # ISO date YYYY-MM-DD
    note: Optional[str] = None


class Entry(EntryCreate):
    id: int
    created_at: Optional[str]


class Summary(BaseModel):
    total_income: float
    total_expense: float
    balance: float
