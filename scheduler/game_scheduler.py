from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.database import AsyncSessionLocal
from database.game_models import GameSession
from sqlalchemy import select
import datetime

scheduler = AsyncIOScheduler()

async def expire_stale_sessions(timeout_seconds: int = 3600):
    cutoff = datetime.datetime.utcnow() - datetime.timedelta(seconds=timeout_seconds)
    async with AsyncSessionLocal() as s:
        q = await s.execute(select(GameSession).where(GameSession.status=='ACTIVE', GameSession.updated_at < cutoff))
        rows = q.scalars().all()
        for r in rows:
            r.status = 'EXPIRED'
            await s.commit()

def start_scheduler():
    scheduler.add_job(expire_stale_sessions, 'interval', minutes=10)
    scheduler.start()
