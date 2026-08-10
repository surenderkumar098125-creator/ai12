from __future__ import annotations
from database.database import AsyncSessionLocal
from database.game_extra_models import PlayerStats, UserBadge
from sqlalchemy import select

async def get_profile(user_id: int):
    async with AsyncSessionLocal() as s:
        q = await s.execute(select(PlayerStats).where(PlayerStats.user_id==user_id))
        stats = q.scalars().first()
        q2 = await s.execute(select(UserBadge).where(UserBadge.user_id==user_id))
        badges = q2.scalars().all()
        return {"stats": stats, "badges": badges}
