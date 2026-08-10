from __future__ import annotations
from database.database import AsyncSessionLocal
from database.game_models import GameScore, GameSession
from database.game_extra_models import FavoriteGame, RecentPlay, GameAnalytics
from sqlalchemy import select, func
import datetime

async def mark_favorite(user_id: int, game_id: str):
    async with AsyncSessionLocal() as s:
        # upsert favorite
        q = await s.execute(select(FavoriteGame).where(FavoriteGame.user_id==user_id, FavoriteGame.game_id==game_id))
        ex = q.scalars().first()
        if ex:
            return ex
        fav = FavoriteGame(user_id=user_id, game_id=game_id)
        s.add(fav)
        await s.commit()
        await s.refresh(fav)
        return fav

async def remove_favorite(user_id: int, game_id: str):
    async with AsyncSessionLocal() as s:
        await s.execute("DELETE FROM favorite_games WHERE user_id = :uid AND game_id = :gid", {"uid": user_id, "gid": game_id})
        await s.commit()
        return True

async def recent_play(user_id: int, game_id: str, score: int = 0):
    async with AsyncSessionLocal() as s:
        q = await s.execute(select(RecentPlay).where(RecentPlay.user_id==user_id, RecentPlay.game_id==game_id))
        r = q.scalars().first()
        if not r:
            r = RecentPlay(user_id=user_id, game_id=game_id, last_played=datetime.datetime.utcnow(), best_score=score)
            s.add(r)
        else:
            r.last_played = datetime.datetime.utcnow()
            if score > (r.best_score or 0):
                r.best_score = score
        await s.commit()
        return r

async def get_trending(limit: int = 10, days: int = 7):
    cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=days)
    async with AsyncSessionLocal() as s:
        q = await s.execute(select(GameAnalytics.game_id, func.sum(GameAnalytics.plays).label('plays')).where(GameAnalytics.date>=cutoff).group_by(GameAnalytics.game_id).order_by(func.sum(GameAnalytics.plays).desc()).limit(limit))
        return [r[0] for r in q.fetchall()]

async def record_analytics(game_id: str, score: int, user_id: int, won: bool):
    d = datetime.datetime.utcnow().date()
    async with AsyncSessionLocal() as s:
        q = await s.execute(select(GameAnalytics).where(func.date(GameAnalytics.date)==d, GameAnalytics.game_id==game_id))
        ga = q.scalars().first()
        if not ga:
            ga = GameAnalytics(game_id=game_id, date=datetime.datetime.utcnow(), plays=1, unique_players=1 if user_id else 0, wins=1 if won else 0, total_score=score, highest_score=score, completions=1)
            s.add(ga)
        else:
            ga.plays = (ga.plays or 0) + 1
            ga.total_score = (ga.total_score or 0) + score
            if score > (ga.highest_score or 0):
                ga.highest_score = score
            if won:
                ga.wins = (ga.wins or 0) + 1
            ga.completions = (ga.completions or 0) + 1
        await s.commit()
