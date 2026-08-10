from database.database import AsyncSessionLocal
from games.registry import GAME_REGISTRY
from games.base import BaseGame
from database.game_models import GameSession, GameScore
from database.database import AsyncSessionLocal
from sqlalchemy import select
import uuid
import datetime

class GameService:
    def __init__(self):
        self.registry = GAME_REGISTRY

    async def start_game_for_user(self, gid: str, user_id: int, group_id: int | None = None, difficulty: str = "normal"):
        cls = self.registry.get_game(gid)
        if not cls:
            raise ValueError("Game not found")
        game = cls()
        init = await game.start()
        state = init.get("state", {})
        session_id = str(uuid.uuid4())
        now = datetime.datetime.utcnow()
        async with AsyncSessionLocal() as s:
            gs = GameSession(session_id=session_id, user_id=user_id, group_id=group_id, game_id=gid, difficulty=difficulty, state=state, status="ACTIVE", started_at=now, updated_at=now)
            s.add(gs)
            await s.commit()
            await s.refresh(gs)
        return {"session_id": session_id, "message": init.get("message","")}

    async def submit_input(self, session_id: str, user_id: int, user_input: any):
        async with AsyncSessionLocal() as s:
            q = await s.execute(select(GameSession).where(GameSession.session_id==session_id))
            sess = q.scalars().first()
            if not sess:
                raise ValueError("Session not found")
            cls = self.registry.get_game(sess.game_id)
            if not cls:
                raise ValueError("Game class not found")
            game = cls()
            result = await game.handle_input(sess.state, user_input)
            sess.state = result.get("state", sess.state)
            sess.updated_at = datetime.datetime.utcnow()
            if result.get("finished"):
                sess.status = "COMPLETED"
                score = game.calculate_score(sess.state)
                sess.score = score
                sess.finished_at = datetime.datetime.utcnow()
                s.add(sess)
                await s.commit()
                # persist score
                gs = GameScore(user_id=sess.user_id, game_id=sess.game_id, group_id=sess.group_id, score=score, difficulty=sess.difficulty, duration=None)
                s.add(gs)
                await s.commit()
            else:
                s.add(sess)
                await s.commit()
            return result
