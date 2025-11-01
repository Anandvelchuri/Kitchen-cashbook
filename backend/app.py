from fastapi import FastAPI, HTTPException, Depends, Query, APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import date
import sqlite3
import os

from . import db
from backend.schemas import EntryCreate, Entry, Summary

# Create the main application
app = FastAPI(title="Veena's Kitchen Cashbook")

# Create API router for /api endpoints
api_router = APIRouter(prefix="/api")

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"\nRequest: {request.method} {request.url.path}")
    try:
        response = await call_next(request)
        print(f"Response status: {response.status_code}")
        return response
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function
def dict_from_row(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

# API Routes
@api_router.post("/entries", response_model=Entry)
async def create_entry(payload: EntryCreate):
    print(f"Creating entry: {payload}")
    if payload.type not in ("income", "expense"):
        raise HTTPException(status_code=400, detail="type must be 'income' or 'expense'")
    try:
        _ = date.fromisoformat(payload.date)
    except Exception:
        raise HTTPException(status_code=400, detail="date must be YYYY-MM-DD")

    with db.get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO entries (type, amount, category, date, item, note) VALUES (?, ?, ?, ?, ?, ?)",
            (payload.type, payload.amount, payload.category, payload.date, getattr(payload, 'item', None), payload.note),
        )
        entry_id = cur.lastrowid
        cur.execute("SELECT id, type, amount, category, date, item, note, created_at FROM entries WHERE id=?", (entry_id,))
        row = cur.fetchone()
        return Entry(**dict_from_row(cur, row))

@api_router.get("/entries", response_model=List[Entry])
async def list_entries(
    type: Optional[str] = Query(None, pattern="^(income|expense)$"),
    start: Optional[str] = None,
    end: Optional[str] = None,
    limit: int = 100
):
    print("Listing entries")
    try:
        q = "SELECT id, type, amount, category, date, item, note, created_at FROM entries"
        clauses = []
        params = []
        if type:
            clauses.append("type = ?")
            params.append(type)
        if start:
            clauses.append("date >= ?")
            params.append(start)
        if end:
            clauses.append("date <= ?")
            params.append(end)
        if clauses:
            q += " WHERE " + " AND ".join(clauses)
        q += " ORDER BY date DESC LIMIT ?"
        params.append(limit)

        with db.get_db() as conn:
            cur = conn.cursor()
            cur.execute(q, tuple(params))
            rows = cur.fetchall()
            entries = [Entry(**dict_from_row(cur, r)) for r in rows]
            print(f"Found {len(entries)} entries")
            return entries
    except Exception as e:
        print(f"Error listing entries: {str(e)}")
        return []

@api_router.get("/summary", response_model=Summary)
async def get_summary(month: Optional[str] = None):
    print(f"Getting summary for month: {month}")
    q = "SELECT type, SUM(amount) FROM entries"
    params = []
    if month:
        q += " WHERE date LIKE ?"
        params.append(f"{month}%")
    q += " GROUP BY type"

    total_income = 0.0
    total_expense = 0.0
    with db.get_db() as conn:
        cur = conn.cursor()
        cur.execute(q, tuple(params))
        for row in cur.fetchall():
            t, s = row
            if t == "income":
                total_income = s or 0.0
            else:
                total_expense = s or 0.0

    return Summary(
        total_income=total_income,
        total_expense=total_expense,
        balance=total_income - total_expense
    )

# Initialize database
@app.on_event("startup")
async def startup():
    print("Initializing database...")
    db.init_db()
    print("Database initialized successfully")

# Mount API routes
app.include_router(api_router)

# Mount static files last
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "static")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")