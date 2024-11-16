from config import TOKEN
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import User

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


from aiogram_translation import Translator

from locales import *
from db.models import db

async def userLang(user: User, bot: Bot) -> str:
    return await db.getUserLang(tg_id=user.id)

translator = Translator(default_language_key="ru", extract_language_function=userLang)

translator.include([
    Russian(),
    English()
])
translator.set_default(key='ru')