from __future__ import annotations
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event, text
from config import settings
import os
from pathlib import Path

DATABASE_URL = settings.DATABASE_URL
echo = False

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=echo,
    future=True,
    pool_pre_ping=True,
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


# For SQLite we set pragmas on connect
def _set_sqlite_pragma(dbapi_conn, conn_record):
    try:
        cursor = dbapi_conn.cursor()
        # Enable foreign keys
        cursor.execute("PRAGMA foreign_keys=ON;")
        # Enable WAL mode
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.close()
    except Exception:
        # non-sqlite DBs will fail here — ignore
        pass

# Attach to the synchronous engine underlying the async engine
try:
    event.listen(engine.sync_engine, "connect", _set_sqlite_pragma)
except Exception:
    # In some runtime contexts (e.g., tests) engine might be not fully configured — ignore safely
    pass

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

# Simple health check helper
async def check_database() -> bool:
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
