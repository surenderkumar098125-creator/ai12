from __future__ import annotations
from typing import List, Optional
from aiogram import Bot
from config import settings
from database.database import AsyncSessionLocal
from database.content_models import Broadcast, BroadcastLog
from sqlalchemy import select
import asyncio
import math
import logging

logger = logging.getLogger("preeti.broadcast")

async def send_broadcast(broadcast_id: int) -> dict:
    """Send a broadcast by id. Returns summary dict."""
    bot = Bot(token=settings.BOT_TOKEN)
    async with AsyncSessionLocal() as s:
        q = await s.execute(select(Broadcast).where(Broadcast.id == broadcast_id))
        b = q.scalars().first()
        if not b:
            raise ValueError("Broadcast not found")
        # For demo, only support audience=all_users and content as text
        if b.audience == "all_users":
            # Fetch user list - simplified: assume users table contains telegram_id
            users_q = await s.execute("SELECT telegram_id FROM users")
            user_rows = users_q.fetchall()
            user_ids = [r[0] for r in user_rows]
        else:
            user_ids = []
        sent = 0
        failed = 0
        blocked = 0
        # batch sends with small delay to avoid floods
        for uid in user_ids:
            try:
                await bot.send_message(uid, b.content)
                sent += 1
                log = BroadcastLog(broadcast_id=b.id, target_type="user", target_id=uid, status="sent")
                s.add(log)
                await s.commit()
            except Exception as e:
                failed += 1
                logger.debug("Failed sending to %s: %s", uid, e)
                log = BroadcastLog(broadcast_id=b.id, target_type="user", target_id=uid, status="failed", error=str(e))
                s.add(log)
                await s.commit()
                await asyncio.sleep(0.05)
        # update broadcast status
        b.status = "completed"
        await s.commit()
        return {"sent": sent, "failed": failed, "blocked": blocked}
