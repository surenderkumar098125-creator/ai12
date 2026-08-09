from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def game_center_keyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚡ ACTION", callback_data="games:category:action"), InlineKeyboardButton(text="🧠 PUZZLE", callback_data="games:category:puzzle")],
        [InlineKeyboardButton(text="🎯 SKILL", callback_data="games:category:skill"), InlineKeyboardButton(text="🏆 CLASSIC", callback_data="games:category:classic")],
        [InlineKeyboardButton(text="😂 FUN", callback_data="games:category:fun"), InlineKeyboardButton(text="👻 HORROR", callback_data="games:category:horror")],
        [InlineKeyboardButton(text="🎲 RANDOM GAME", callback_data="games:random"), InlineKeyboardButton(text="🏆 LEADERBOARD", callback_data="games:leaderboard")]
    ])
    return kb
