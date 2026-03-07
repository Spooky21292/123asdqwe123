import asyncio

from aiogram import Bot


class ReminderService:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def schedule_reminder(
        self,
        user_id: int,
        video_title: str,
        video_url: str,
        delay_minutes: int = 60,
    ) -> None:
        asyncio.create_task(self._reminder_task(user_id, video_title, video_url, delay_minutes))

    async def _reminder_task(
        self,
        user_id: int,
        video_title: str,
        video_url: str,
        delay_minutes: int,
    ) -> None:
        await asyncio.sleep(delay_minutes * 60)
        await self.bot.send_message(
            user_id,
            f"🔔 Напоминание\n\nНе забудьте посмотреть:\n{video_title}\n{video_url}",
        )
