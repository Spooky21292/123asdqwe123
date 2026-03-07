from datetime import datetime

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.models import User
from database.session import Database
from keyboards.inline import mark_habit_keyboard
from repositories.habits import HabitRepository
from services.habit_service import HabitService
from utils.datetime_utils import parse_timezone


async def dispatch_habit_reminders(bot: Bot, db: Database) -> None:
    now_utc = datetime.utcnow()

    async with db.session_factory() as session:
        habit_repo = HabitRepository(session)
        habits = await habit_repo.habits_for_reminders()

        for habit in habits:
            user = await session.get(User, habit.user_id)
            if not user or not user.reminders_enabled:
                continue

            tz = parse_timezone(user.timezone)
            local_dt = now_utc.astimezone(tz)
            if not habit.reminder_time:
                continue
            if (
                local_dt.hour == habit.reminder_time.hour
                and local_dt.minute == habit.reminder_time.minute
                and HabitService.is_habit_scheduled_for_date(habit, local_dt.date())
            ):
                await bot.send_message(
                    chat_id=user.telegram_id,
                    text=f"🔔 Напоминание: {habit.title}\nОтметишь сейчас?",
                    reply_markup=mark_habit_keyboard(habit.id),
                )


def setup_scheduler(bot: Bot, db: Database) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(dispatch_habit_reminders, "cron", second=0, args=[bot, db], id="habit_reminders", replace_existing=True)
    scheduler.start()
    return scheduler
