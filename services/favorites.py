from __future__ import annotations
from database.database import AsyncSessionLocal
from database.game_extra_models import FavoriteGame
from sqlalchemy import select

async def add_favorite(user_id: int, game_id: str):
    async with AsyncSessionLocal() as s:
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

async def list_favorites(user_id: int, limit: int = 20, offset: int = 0):
    async with AsyncSessionLocal() as s:
        q = await s.execute(select(FavoriteGame).where(FavoriteGame.user_id==user_id).order_by(FavoriteGame.added_at.desc()).limit(limit).offset(offset))
        return q.scalars().all()
