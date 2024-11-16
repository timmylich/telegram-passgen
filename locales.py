from aiogram_translation.models import BaseTranslationBuilder
from config import Repo

class BaseTranslation(BaseTranslationBuilder):
    info: str
    input_error: str
    input_lenght_error: str

class Russian(BaseTranslation):
    key: str = "ru"
    name: str = "Русский"

    info: str = """🔑Генерируйте пароли с помощью бота.
Отправьте сообщение с длиной пароля и ключевым словом через запятую.

❗Например:
* 8, abcedf
* 12-16, alex1999
* 10

📃Бот не хранит никаких данных, кроме ID пользователя и его языка.
🌐Открытый исходный код: %s""" % (Repo)

    input_error: str = "❌Неверный формат, следуйте примерам."
    input_lenght_error: str = "❌Минимальная длина не может быть больше максимальной."


class English(Russian):
    key: str = "en"
    name: str = "English"

    info: str = """🔑Generate passwords using the bot.
Send a message with the password length and a keyword separated by a comma.

❗For example:
* 8, abcdef
* 12-16, alex1999
* 10

📃The bot does not store any data except the user ID and their language.
🌐Open Source Code: %s""" % (Repo)

    input_error: str = "❌Invalid format, please follow the examples."
    input_length_error: str = "❌The minimum length cannot be greater than the maximum length."
