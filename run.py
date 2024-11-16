import asyncio, logging, sys
from aiogram import Dispatcher


from bot import bot, translator
from app.hls import router as hls_router

dp = Dispatcher()
translator.register(dp)

async def main():
    dp.include_router(hls_router)

    await dp.start_polling(bot)

        
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot disabled.")
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        