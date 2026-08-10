from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards.game_center import game_center_keyboard
from services.discovery import get_trending
from services.favorites import list_favorites
from games.registry import GAME_REGISTRY
from config import settings
import logging

router = Router()
logger = logging.getLogger("preeti.handlers.game_center")

@router.message(Command("games"))
async def cmd_games(message: Message):
    await message.reply("🎮 PREETI GAME CENTER", reply_markup=game_center_keyboard())

@router.callback_query()
async def game_center_callbacks(query: CallbackQuery):
    data = query.data or ""
    if not data.startswith('gc:'):
        await query.answer()
        return
    action = data.split(':',1)[1]
    if action == 'trending':
        trending = await get_trending()
        text = "🔥 Trending Games:\n" + '\n'.join(trending[:10])
        await query.message.answer(text)
    elif action == 'favorites':
        user_id = query.from_user.id
        favs = await list_favorites(user_id)
        text = "⭐ Your Favorites:\n" + '\n'.join([f.game_id for f in favs]) if favs else "You have no favorites."
        await query.message.answer(text)
    elif action == 'random':
        g = GAME_REGISTRY.random_game()
        if g:
            await query.message.answer(f"🎲 Random Game: {g.get_name()} (id: {g.get_id()})")
        else:
            await query.message.answer("No games available.")
    else:
        await query.message.answer(f"Not implemented: {action}")
    await query.answer()
