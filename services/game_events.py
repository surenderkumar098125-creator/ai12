from database.database import AsyncSessionLocal
from database.game_models import GameSession, GameScore
from database.models import UserAchievement
from services.game_leaderboard import LeaderboardService
from services.reward_manager import RewardManager
from services.challenge_service import ChallengeService
from games.anti_cheat import AntiCheat
from sqlalchemy import select
import datetime

class GameEvents:
    def __init__(self):
        self.leaderboard = LeaderboardService()
        self.rewards = RewardManager()
        self.challenges = ChallengeService()

    async def on_game_completed(self, session_id: str):
        async with AsyncSessionLocal() as s:
            q = await s.execute(select(GameSession).where(GameSession.session_id==session_id))
            sess = q.scalars().first()
            if not sess:
                return
            # anti-cheat
            if not AntiCheat.validate_score(sess.game_id, sess.score, 0):
                # flag
                return
            # create GameScore
            gs = GameScore(user_id=sess.user_id, game_id=sess.game_id, group_id=sess.group_id, score=sess.score, difficulty=sess.difficulty, duration=None)
            s.add(gs)
            await s.commit()
            await s.refresh(gs)
            # reward
            reward = sess.state.get('reward')
            if not reward:
                # calculate reward via game's calculate_reward not available here, assume coins based on score
                coins = max(1, sess.score//10)
                xp = max(1, coins//2)
                gems = 0
            else:
                coins = reward.get('coins',0)
                xp = reward.get('xp',0)
                gems = reward.get('gems',0)
            await self.rewards.award(sess.session_id, sess.user_id, coins, xp, gems)
            # achievements - simplified: first game
            q2 = await s.execute(select(UserAchievement).where(UserAchievement.user_id==sess.user_id))
            existing = q2.scalars().first()
            if not existing:
                ua = UserAchievement(user_id=sess.user_id, achievement_id=1)
                s.add(ua)
                await s.commit()
