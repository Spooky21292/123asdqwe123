import asyncio

from aiogram import Bot, Dispatcher, Router

from bot.config import get_settings
from bot.database import Database
from bot.handlers import setup_handlers
from bot.playlists import setup_playlist_handlers
from bot.reminders import ReminderService


async def main() -> None:
    settings = get_settings()
    db = Database(settings.database_path)
    await db.init()

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    router = Router()

    reminder_service = ReminderService(bot)

    setup_handlers(router, db=db, settings=settings, reminder_service=reminder_service)
    setup_playlist_handlers(router)

    dp.include_router(router)

    # Простая инъекция БД для плейлист-хендлеров
    dp["db"] = db

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
