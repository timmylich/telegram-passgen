from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

def get_language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇬🇧🇺🇸English", callback_data='lang_en')],
        [InlineKeyboardButton(text="🇷🇺Русский", callback_data='lang_ru')]
    ])