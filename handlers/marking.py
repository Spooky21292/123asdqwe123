from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from database.models import HabitStatus
from database.session import Database
from keyboards.inline import mark_habit_keyboard
from keyboards.reply import MAIN_MENU_TEXTS
from repositories.habits import HabitRepository
from repositories.users import UserRepository
from services.habit_service import HabitService
from utils.datetime_utils import local_today

router = Router()


@router.message(F.text == MAIN_MENU_TEXTS["mark_today"])
async def mark_today(message: Message, db: Database) -> None:
    async with db.session_factory() as session:
        user = await UserRepository(session).get_by_telegram_id(message.from_user.id)
        if not user:
            await message.answer("Нажми /start")
            return

        habit_repo = HabitRepository(session)
        service = HabitService(habit_repo)
        habits = await service.habits_for_today(user.id, user.timezone)

    if not habits:
        await message.answer("На сегодня привычек нет. Можно выдохнуть 😌")
        return

    for habit in habits:
        await message.answer(f"{habit.title}\nВыбери статус за сегодня:", reply_markup=mark_habit_keyboard(habit.id))


@router.callback_query(F.data.startswith("habit_mark:"))
async def mark_habit(callback: CallbackQuery, db: Database) -> None:
    _, habit_id_raw, status_raw = callback.data.split(":")
    habit_id = int(habit_id_raw)
    status = HabitStatus(status_raw)

    async with db.session_factory() as session:
        user = await UserRepository(session).get_by_telegram_id(callback.from_user.id)
        if not user:
            await callback.answer("Нажми /start", show_alert=True)
            return

        repo = HabitRepository(session)
        habit = await repo.get_by_id(habit_id, user.id)
        if not habit:
            await callback.answer("Привычка не найдена", show_alert=True)
            return

        today = local_today(user.timezone)
        await repo.upsert_log(habit.id, user.id, today, status)

        service = HabitService(repo)
        current_streak, _ = await service.calculate_streak(habit, user.timezone)

    status_text = {
        HabitStatus.DONE: "выполненной ✅",
        HabitStatus.MISSED: "не выполненной ❌",
        HabitStatus.LATER: "отложенной ⏰",
    }[status]

    text = (
        f"Привычка «{habit.title}» отмечена как {status_text}\n"
        f"Текущий стрик: {current_streak} дней 🔥"
    )

    await callback.message.edit_text(f"{habit.title}\nСтатус обновлён ✅", reply_markup=mark_habit_keyboard(habit.id))
    await callback.message.answer(text)
    await callback.answer()
