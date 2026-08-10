from __future__ import annotations
from database.database import AsyncSessionLocal
from database.game_extra_models import RecentPlay
from sqlalchemy import select

async def list_recent(user_id: int, limit: int = 20):
    async with AsyncSessionLocal() as s:
        q = await s.execute(select(RecentPlay).where(RecentPlay.user_id==user_id).order_by(RecentPlay.last_played.desc()).limit(limit))
        return q.scalars().all()
