from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import Command
from locales import *
from bot import bot
from db.models import db
from app.kb import get_language_keyboard
import random, re

router = Router()

@router.message(Command("start"))
@router.message(Command("lang"))
async def start(message: Message):
    await db.insertUser(tg_id=message.from_user.id)
    await message.answer(text="🇬🇧🇺🇸Choose language.\n\n🇷🇺Выберите язык.", reply_markup=get_language_keyboard())

import random

def generate_password(length: int, keyword: str) -> str:
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    
    replacements = {'a': '@', 's': '$', 'o': '0'}
    
    modified_keyword = "".join(
        random.choice([replacements.get(char, char), char]) for char in keyword
    )
    
    remaining_length = length - len(modified_keyword)
    if remaining_length < 0:
        raise ValueError("Длина пароля меньше длины ключевого слова.")
    
    random_chars = "".join(random.choice(characters) for _ in range(length))
    
    start = int(random.randint(0, length-len(modified_keyword) ))
    password = random_chars.replace(random_chars[start : start+len(modified_keyword) ], modified_keyword) 
    
    password = list(password)
    random.shuffle(password[len(modified_keyword):])
    
    return "".join(password)

print(generate_password(15, "alex"))

@router.message()
async def generate_passwords(message: Message, language: BaseTranslation):
    user_input = message.text
    pattern = re.compile(r"^(\d{1,2})(?:-(\d{1,2}))?(?:,\s*(\w+))?$")
    match = pattern.match(user_input)

    if not match:
        await message.reply(language.input_error)
        return

    min_length = int(match.group(1))
    max_length = int(match.group(2)) if match.group(2) else min_length
    keyword = match.group(3) or ""

    if min_length > max_length:
        await message.reply(language.input_lenght_error)
        return

    passwords = ["<code>"+ generate_password(random.randint(min_length, max_length), keyword)  +"</code>" for _ in range(5)]

    await message.reply("\n".join(passwords))




@router.callback_query(F.data.startswith('lang_'))
async def process_language_selection(callback: CallbackQuery, language: BaseTranslation):
    language_code = callback.data.split('_')[1]

    # Сохранение выбранного языка в базе данных
    await db.setUserLang(tg_id=callback.from_user.id, lang=language_code)

    # Отправка подтверждающего сообщения
    if language_code == 'en':
        language = English()
        response_text = "🇬🇧🇺🇸Language is set to English.\n\n❗The translation was made using an automatic translator and may contain errors and inaccuracies."
    elif language_code == 'ru':
        language = Russian()
        response_text = "🇷🇺Установлен Русский язык."

    await bot.send_message(chat_id=callback.from_user.id, text=response_text)
    await callback.answer()

    await bot.send_message(chat_id=callback.from_user.id, text=language.info, disable_web_page_preview=True)