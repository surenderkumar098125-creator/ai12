from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List

def admin_main_keyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚙️ BOT SETTINGS", callback_data="admin:bot_settings")],
        [InlineKeyboardButton(text="👋 WELCOME", callback_data="admin:welcome")],
        [InlineKeyboardButton(text="📢 BROADCAST", callback_data="admin:broadcast")],
        [InlineKeyboardButton(text="📝 MESSAGES", callback_data="admin:messages")],
        [InlineKeyboardButton(text="💾 BACKUP", callback_data="admin:backup")]
    ])
    return kb

def welcome_edit_keyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Edit Message", callback_data="welcome:edit_message")],
        [InlineKeyboardButton(text="🖼️ Set Image", callback_data="welcome:set_image")],
        [InlineKeyboardButton(text="🔘 Buttons", callback_data="welcome:buttons")],
        [InlineKeyboardButton(text="👁 Preview", callback_data="welcome:preview")],
        [InlineKeyboardButton(text="💾 Save", callback_data="welcome:save")]
    ])
    return kb
