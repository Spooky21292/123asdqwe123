import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import Settings
from database.session import Database
from handlers import errors, goals, habits, marking, notes, settings, start, stats
from scheduler.reminders import setup_scheduler


async def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    settings_data = Settings.from_env()
    db = Database(settings_data.database_url)
    await db.create_tables()

    bot = Bot(token=settings_data.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(habits.router)
    dp.include_router(marking.router)
    dp.include_router(stats.router)
    dp.include_router(goals.router)
    dp.include_router(notes.router)
    dp.include_router(settings.router)
    dp.include_router(errors.router)

    scheduler = setup_scheduler(bot, db)

    try:
        await dp.start_polling(bot, db=db)
    finally:
        scheduler.shutdown(wait=False)
        await db.dispose()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
