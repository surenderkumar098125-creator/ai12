"""
Development migration runner.

This is a simple create_all migration convenience for local development.
For production use Alembic migration scripts.

Usage:
    python main.py migrate
"""
import asyncio
from database import database
from database.models import Base
from sqlalchemy.ext.asyncio import AsyncEngine

async def upgrade():
    print("Running development migration (create_all).")
    async with database.engine.begin() as conn:
        # run create_all in sync context via run_sync
        await conn.run_sync(Base.metadata.create_all)
    print("Migration complete.")

async def downgrade():
    print("Dropping all tables (development only!).")
    async with database.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    print("Dropped all tables.")
