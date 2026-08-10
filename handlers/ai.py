from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from services.ai_behavior import ask_ai
from services.context_manager import get_or_create_conversation, clear_conversation
from config import settings
import logging

router = Router()
logger = logging.getLogger("preeti.handlers.ai")

@router.message(Command("ai"))
async def cmd_ai(message: Message):
    # /ai <text> or reply
    user_id = message.from_user.id
    conversation_id = f"user:{user_id}"
    text = (message.text or "").partition(" ")[2].strip()
    if not text and message.reply_to_message:
        text = message.reply_to_message.text or ""
    if not text:
        await message.reply("Please provide a question after /ai or reply to a message.")
        return
    resp = await ask_ai(user_id, conversation_id, text)
    await message.reply(resp)

@router.message(Command("chat"))
async def cmd_chat(message: Message):
    # /chat just forwards message to AI and keeps context
    user_id = message.from_user.id
    conversation_id = f"user:{user_id}"
    text = (message.text or "").partition(" ")[2].strip()
    if not text and message.reply_to_message:
        text = message.reply_to_message.text or ""
    if not text:
        await message.reply("Usage: /chat <message> (keeps conversation context)")
        return
    resp = await ask_ai(user_id, conversation_id, text)
    await message.reply(resp)

@router.message(Command("clear"))
async def cmd_clear(message: Message):
    user_id = message.from_user.id
    conversation_id = f"user:{user_id}"
    conv = await get_or_create_conversation(conversation_id, user_id)
    await clear_conversation(conv)
    await message.reply("Conversation cleared.")

@router.message()
async def mention_or_reply(message: Message):
    # If bot is mentioned or directly replied to, handle with AI but rate-limited elsewhere
    if message.reply_to_message and message.reply_to_message.from_user and message.reply_to_message.from_user.is_bot:
        # likely replying to bot
        user_id = message.from_user.id
        conversation_id = f"user:{user_id}"
        text = message.text or ""
        if not text:
            return
        resp = await ask_ai(user_id, conversation_id, text)
        await message.reply(resp)
    elif message.entities:
        # detect mention of bot username (skipped due to lacking bot username here)
        return
