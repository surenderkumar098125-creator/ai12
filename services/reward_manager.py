from __future__ import annotations
from database.database import AsyncSessionLocal
from database.game_models import GameScore, GameSession, RewardRecord
from database.models import Wallet, Transaction
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import datetime

class RewardManager:
    """Atomic reward issuance with idempotency based on session_id"""
    async def award(self, session_id: str, user_id: int, coins: int, xp: int, gems: int) -> bool:
        async with AsyncSessionLocal() as s:
            # load session
            q = await s.execute(select(GameSession).where(GameSession.session_id == session_id))
            gs = q.scalars().first()
            if not gs:
                return False
            if gs.status != 'COMPLETED':
                return False
            # idempotency check via RewardRecord table
            qrr = await s.execute(select(RewardRecord).where(RewardRecord.session_id == session_id))
            existing = qrr.scalars().first()
            if existing:
                return True
            try:
                # begin transaction
                # fetch or create wallet
                q3 = await s.execute(select(Wallet).where(Wallet.user_id == gs.user_id))
                wal = q3.scalars().first()
                if not wal:
                    wal = Wallet(user_id=gs.user_id, coins=0, gems=0, xp=0)
                    s.add(wal)
                    await s.flush()
                wal.coins = wal.coins + coins
                wal.gems = wal.gems + gems
                wal.xp = wal.xp + xp
                # insert transaction record(s)
                t = Transaction(user_id=gs.user_id, amount=coins, currency='coins', reason='game_reward', metadata={'session_id': session_id})
                s.add(t)
                # insert reward record for idempotency
                rr = RewardRecord(session_id=session_id, user_id=gs.user_id, coins=coins, gems=gems, xp=xp)
                s.add(rr)
                await s.commit()
                return True
            except Exception:
                await s.rollback()
                return False
