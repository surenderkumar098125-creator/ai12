from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from games.registry import GAME_REGISTRY
from keyboards.games import game_center_keyboard
from services.game_service import GameService
import logging

router = Router()
logger = logging.getLogger("preeti.handlers.games")

@router.message(Command("games"))
async def cmd_games(message: Message):
    # Show game center
    await message.reply("🎮 PREETI GAME CENTER", reply_markup=game_center_keyboard())

@router.message(Command("play"))
async def cmd_play(message: Message):
    # /play <game_id>
    args = (message.text or "").split(maxsplit=1)
    if len(args) < 2:
        await message.reply("Usage: /play <game_id>")
        return
    gid = args[1].strip()
    svc = GameService()
    try:
        res = await svc.start_game_for_user(gid, message.from_user.id)
        await message.reply(res.get("message", "Game started"))
    except Exception as e:
        await message.reply(f"Error: {e}")
