from database.database import AsyncSessionLocal
from database.game_models import GameScore
from sqlalchemy import select, func

class LeaderboardService:
    async def top_global(self, game_id: str, limit: int = 10):
        async with AsyncSessionLocal() as s:
            q = await s.execute(select(GameScore.user_id, func.max(GameScore.score).label('score')).where(GameScore.game_id==game_id).group_by(GameScore.user_id).order_by(func.max(GameScore.score).desc()).limit(limit))
            return q.fetchall()

    async def personal_best(self, user_id: int, game_id: str):
        async with AsyncSessionLocal() as s:
            q = await s.execute(select(func.max(GameScore.score)).where(GameScore.game_id==game_id, GameScore.user_id==user_id))
            return q.scalar()
