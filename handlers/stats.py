from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from database.session import Database
from keyboards.inline import stats_habits_keyboard
from keyboards.reply import MAIN_MENU_TEXTS
from repositories.habits import HabitRepository
from repositories.users import UserRepository
from services.habit_service import HabitService

router = Router()


@router.message(F.text == MAIN_MENU_TEXTS["stats"])
async def stats_menu(message: Message, db: Database) -> None:
    async with db.session_factory() as session:
        user = await UserRepository(session).get_by_telegram_id(message.from_user.id)
        habits = await HabitRepository(session).get_user_habits(user.id)

    if not habits:
        await message.answer("Нет привычек для статистики.")
        return

    await message.answer("Выбери привычку для детальной статистики:", reply_markup=stats_habits_keyboard(habits))


@router.callback_query(F.data.startswith("habit_stats:"))
async def habit_stats(callback: CallbackQuery, db: Database) -> None:
    habit_id = int(callback.data.split(":")[1])
    async with db.session_factory() as session:
        user = await UserRepository(session).get_by_telegram_id(callback.from_user.id)
        repo = HabitRepository(session)
        habit = await repo.get_by_id(habit_id, user.id)
        if not habit:
            await callback.answer("Привычка не найдена", show_alert=True)
            return

        stats = await HabitService(repo).calculate_stats(habit, user.timezone)

    p7 = int((stats.done_7 / stats.total_7) * 100) if stats.total_7 else 0
    p30 = int((stats.done_30 / stats.total_30) * 100) if stats.total_30 else 0

    text = (
        f"📊 <b>Статистика: {habit.title}</b>\n\n"
        f"За 7 дней: {stats.done_7}/{stats.total_7} ({p7}%)\n"
        f"За 30 дней: {stats.done_30}/{stats.total_30} ({p30}%)\n"
        f"Текущий стрик: {stats.current_streak} 🔥\n"
        f"Лучший стрик: {stats.best_streak} 🏆\n"
        f"Всего выполнено: {stats.total_done} раз"
    )
    await callback.message.answer(text)
    await callback.answer()
