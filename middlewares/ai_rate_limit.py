from aiogram import BaseMiddleware
from aiogram.types import Update
from typing import Callable, Any
from config import settings
from database.database import AsyncSessionLocal
from database.models import AIRequest, UserVIP
import datetime
import logging

logger = logging.getLogger("preeti.ai_rate_limit")

class AIRateLimitMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Update, Any], Any], event: Update, data: dict):
        # Only apply to Message updates
        try:
            user = None
            if event.message:
                user = event.message.from_user
            if not user:
                return await handler(event, data)
            uid = user.id
            # Admins bypass or have higher limits
            admin_ids = getattr(settings, "ADMIN_IDS", [])
            if uid in admin_ids:
                return await handler(event, data)
            # Count today's AIRequest entries
            async with AsyncSessionLocal() as s:
                today = datetime.datetime.utcnow().date()
                q = await s.execute("SELECT COUNT(1) FROM ai_requests WHERE user_id = :uid AND date(created_at) = :today", {"uid": uid, "today": today.isoformat()})
                cnt = q.scalar() or 0
            # Decide limit (VIP vs free) -- simplified: check user VIP existence
            limit = settings.AI_DAILY_LIMIT_FREE
            # TODO: check VIP membership in DB -- for now use free limit
            if cnt >= limit:
                # deny
                if event.message:
                    await event.message.reply("You have reached your daily AI limit.")
                return
            return await handler(event, data)
        except Exception as e:
            logger.exception("Rate limit middleware error")
            return await handler(event, data)
