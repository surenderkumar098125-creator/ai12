from aiogram import Router
from aiogram.types import Message
from config import settings
from database.database import check_database

router = Router()

@router.message(lambda m: m.text and m.text.startswith('/health'))
async def health_cmd(message: Message):
    ok = await check_database()
    text = f"Health:\n - database: {'OK' if ok else 'FAIL'}\n - ai: {'configured' if settings.GROQ_API_KEY else 'not configured'}"
    # only allow admins
    if message.from_user.id not in settings.ADMIN_IDS:
        await message.reply("Unauthorized")
        return
    await message.reply(text)
