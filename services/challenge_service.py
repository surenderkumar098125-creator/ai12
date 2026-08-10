from database.database import AsyncSessionLocal
from database.models import Challenge
from database.game_models import GameSession
from sqlalchemy import select
import datetime

class ChallengeService:
    async def create_challenge(self, challenger_id: int, challenged_id: int, game_id: str, expires_in_seconds: int = 3600):
        if challenger_id == challenged_id:
            raise ValueError("Cannot challenge yourself")
        async with AsyncSessionLocal() as s:
            ch = Challenge(challenger_id=challenger_id, challenged_id=challenged_id, game_id=game_id, expires_at=datetime.datetime.utcnow()+datetime.timedelta(seconds=expires_in_seconds), state='PENDING')
            s.add(ch)
            await s.commit()
            await s.refresh(ch)
            return ch
    async def accept_challenge(self, challenge_id: int, user_id: int):
        async with AsyncSessionLocal() as s:
            q = await s.execute(select(Challenge).where(Challenge.id==challenge_id))
            ch = q.scalars().first()
            if not ch:
                raise ValueError('Challenge not found')
            if ch.challenged_id != user_id:
                raise ValueError('Not authorized')
            if ch.state != 'PENDING':
                raise ValueError('Challenge not pending')
            if ch.expires_at < datetime.datetime.utcnow():
                ch.state = 'EXPIRED'
                await s.commit()
                raise ValueError('Challenge expired')
            ch.state = 'ACCEPTED'
            await s.commit()
            return ch
