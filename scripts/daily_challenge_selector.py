from __future__ import annotations
from database.database import AsyncSessionLocal
from database.game_extra_models import DailyChallenge
from games.registry import GAME_REGISTRY
import datetime

def _date_key(dt: datetime.date) -> str:
    return dt.strftime('%Y-%m-%d')

async def select_daily_challenge():
    today = datetime.datetime.utcnow().date()
    key = _date_key(today)
    async with AsyncSessionLocal() as s:
        # check existing
        from sqlalchemy import select
        q = await s.execute(select(DailyChallenge).where(DailyChallenge.date_key==key))
        dc = q.scalars().first()
        if dc:
            return dc
        # deterministic selection: pick a game based on date hash
        games = GAME_REGISTRY.list_games()
        if not games:
            return None
        idx = (today.toordinal() % len(games))
        game_cls = games[idx]
        dc = DailyChallenge(date_key=key, game_id=game_cls.get_id(), metadata={})
        s.add(dc)
        await s.commit()
        await s.refresh(dc)
        return dc
