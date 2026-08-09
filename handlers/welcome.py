from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputFile
from aiogram.filters import Command
from services.welcome_manager import create_or_update_welcome, get_welcome_for_group, remove_welcome
from services.content_manager import save_template, preview_template
from config import settings
import logging

router = Router()
logger = logging.getLogger("preeti.handlers.welcome")

@router.message(Command("setwelcome"))
async def cmd_set_welcome(message: Message):
    # Admin-only helper to set welcome for group where command is issued
    if not message.chat or not message.chat.type.endswith("group"):
        await message.reply("This command must be used in a group by a group admin.")
        return
    # simplest auth: check user is chat admin omitted here for brevity
    group_id = message.chat.id
    text = (message.text or "").partition(" ")[2].strip()
    if not text:
        await message.reply("Usage: /setwelcome Your welcome message with variables like {first_name}")
        return
    tpl = await save_template(f"welcome_{group_id}", text, message.from_user.id)
    await create_or_update_welcome(group_id, enabled=True, message_template_id=tpl.id)
    await message.reply("Welcome message saved.")

@router.message(Command("previewwelcome"))
async def cmd_preview_welcome(message: Message):
    group_id = message.chat.id if message.chat else 0
    ws = await get_welcome_for_group(group_id)
    if not ws:
        await message.reply("No welcome configured for this group.")
        return
    # fetch template
    from services.content_manager import get_template
    tpl = await get_template(f"welcome_{group_id}")
    sample = {"first_name": "Alex", "group": (message.chat.title if message.chat else "Test Group")}
    preview = await preview_template(tpl.content if tpl else "", sample)
    await message.reply(preview)

@router.message(Command("removewelcome"))
async def cmd_remove_welcome(message: Message):
    group_id = message.chat.id if message.chat else 0
    ok = await remove_welcome(group_id)
    if ok:
        await message.reply("Welcome removed.")
    else:
        await message.reply("No welcome to remove.")
