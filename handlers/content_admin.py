from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards.content_admin import admin_main_keyboard, welcome_edit_keyboard
from config import settings
import logging

router = Router()
logger = logging.getLogger("preeti.handlers.content_admin")

def is_global_admin(user_id: int) -> bool:
    return user_id in getattr(settings, "ADMIN_IDS", [])

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    user_id = message.from_user.id
    if not is_global_admin(user_id):
        await message.reply("You are not authorized to access the admin panel.")
        return
    await message.reply("💗 PREETI ADMIN PANEL", reply_markup=admin_main_keyboard())

@router.callback_query(F.data.startswith("admin:"))
async def admin_callbacks(query: CallbackQuery):
    user_id = query.from_user.id
    if not is_global_admin(user_id):
        await query.answer("Unauthorized", show_alert=True)
        return
    action = query.data.split(":", 1)[1]
    if action == "welcome":
        await query.message.answer("Welcome settings", reply_markup=welcome_edit_keyboard())
    elif action == "broadcast":
        await query.message.answer("Broadcast panel: use /broadcast to create broadcasts")
    else:
        await query.message.answer(f"Not implemented: {action}")
    await query.answer()
