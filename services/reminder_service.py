from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.users import UserRepository


class ReminderService:
    def __init__(self, bot: Bot, session: AsyncSession) -> None:
        self.bot = bot
        self.user_repo = UserRepository(session)

    async def send_habit_reminder(self, telegram_id: int, text: str, keyboard: InlineKeyboardMarkup) -> None:
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user or not user.reminders_enabled:
            return
        await self.bot.send_message(chat_id=telegram_id, text=text, reply_markup=keyboard)
