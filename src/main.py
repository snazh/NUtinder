import asyncio
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from config import bot_settings
from handlers import profile_router, main_router, commands_router
import aioredis



# async def fetch_user_profiles():
#     while True:
#         # Fetch profiles from the database
#         profiles = await get_all_profiles_from_db()
#         # Cache the profiles
#         cache.set("user_profiles", profiles)
#         # Wait for 5 minutes
#         await asyncio.sleep(300)  # 300 seconds = 5 minutes
async def main():
    bot = Bot(token=bot_settings.BOT_TOKEN)
    dispatcher = Dispatcher(storage=MemoryStorage())
    dispatcher.include_router(profile_router)
    dispatcher.include_router(commands_router)
    dispatcher.include_router(main_router)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot is turned off")
