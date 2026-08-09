from aiogram import Router
from aiogram.filters import Command
from services.broadcast_manager import send_broadcast
from config import settings
from database.content_models import Broadcast
from database.database import AsyncSessionLocal
from sqlalchemy import select
import logging

router = Router()
logger = logging.getLogger("preeti.handlers.broadcast")

@router.message(Command("broadcast"))
async def cmd_broadcast(message):
    # Very simple broadcast creation flow for global admins via command
    user_id = message.from_user.id
    admin_ids = getattr(settings, "ADMIN_IDS", [])
    if user_id not in admin_ids:
        await message.reply("Unauthorized")
        return
    # usage: /broadcast <title> | <message>
    payload = (message.text or "").partition(" ")[2]
    if not payload or "|" not in payload:
        await message.reply("Usage: /broadcast Title | Message")
        return
    title, _, content = payload.partition("|")
    async with AsyncSessionLocal() as s:
        b = Broadcast(title=title.strip(), content=content.strip(), audience="all_users", created_by=user_id)
        s.add(b)
        await s.commit()
        await s.refresh(b)
        await message.reply(f"Broadcast created (id={b.id}). Sending...")
        res = await send_broadcast(b.id)
        await message.reply(f"Broadcast result: {res}")
