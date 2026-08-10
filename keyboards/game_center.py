from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def game_center_keyboard(page:int=1, per_page:int=6):
    # simplified static menu with pagination placeholder
    offset = (page-1)*per_page
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Play Now", callback_data="gc:play_now")],
        [InlineKeyboardButton(text="🎲 Random Game", callback_data="gc:random")],
        [InlineKeyboardButton(text="🔥 Trending", callback_data="gc:trending")],
        [InlineKeyboardButton(text="⭐ Favorites", callback_data="gc:favorites")],
        [InlineKeyboardButton(text="🏆 Leaderboards", callback_data="gc:leaderboards")],
        [InlineKeyboardButton(text="📅 Daily Challenge", callback_data="gc:daily")],
        [InlineKeyboardButton(text="⚔️ Challenges", callback_data="gc:challenges")],
        [InlineKeyboardButton(text="📊 My Statistics", callback_data="gc:stats")],
        [InlineKeyboardButton(text="🧩 Categories", callback_data="gc:categories")],
    ])
    return kb
