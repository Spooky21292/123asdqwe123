from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.session import Database
from keyboards.inline import reminder_habits_keyboard
from keyboards.reply import MAIN_MENU_TEXTS
from repositories.habits import HabitRepository
from repositories.users import UserRepository
from states.habit import ReminderTimeState
from states.settings import SettingsState

router = Router()


@router.message(F.text == MAIN_MENU_TEXTS["settings"])
async def open_settings(message: Message) -> None:
    await message.answer(
        "⚙️ Настройки:\n"
        "/timezone — сменить часовой пояс\n"
        "/toggle_reminders — вкл/выкл напоминания глобально"
    )


@router.message(F.text == "/timezone")
async def timezone_start(message: Message, state: FSMContext) -> None:
    await state.set_state(SettingsState.timezone)
    await message.answer("Введи часовой пояс, например Europe/Moscow или Asia/Yekaterinburg")


@router.message(SettingsState.timezone)
async def timezone_save(message: Message, state: FSMContext, db: Database) -> None:
    timezone = message.text.strip()
    async with db.session_factory() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_by_telegram_id(message.from_user.id)
        await user_repo.update_settings(user, timezone=timezone)
    await state.clear()
    await message.answer(f"Часовой пояс обновлён: {timezone} ✅")


@router.message(F.text == "/toggle_reminders")
async def toggle_reminders(message: Message, db: Database) -> None:
    async with db.session_factory() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_by_telegram_id(message.from_user.id)
        updated = await user_repo.update_settings(user, reminders_enabled=not user.reminders_enabled)
    await message.answer(
        f"Глобальные напоминания {'включены' if updated.reminders_enabled else 'выключены'} {'🔔' if updated.reminders_enabled else '🔕'}"
    )


@router.message(F.text == MAIN_MENU_TEXTS["reminders"])
async def reminders_menu(message: Message, db: Database, state: FSMContext) -> None:
    async with db.session_factory() as session:
        user = await UserRepository(session).get_by_telegram_id(message.from_user.id)
        habits = await HabitRepository(session).get_user_habits(user.id, active_only=True)

    habits = [h for h in habits if h.reminder_enabled]
    if not habits:
        await message.answer("Нет активных привычек с напоминаниями.")
        return

    await state.set_state(ReminderTimeState.choose_habit)
    await message.answer("Выбери привычку, чтобы изменить время напоминания:", reply_markup=reminder_habits_keyboard(habits))


@router.callback_query(F.data.startswith("remind_time:"))
async def reminder_choose(callback: CallbackQuery, state: FSMContext) -> None:
    habit_id = int(callback.data.split(":")[1])
    await state.update_data(habit_id=habit_id)
    await state.set_state(ReminderTimeState.new_time)
    await callback.message.answer("Введи новое время (HH:MM):")
    await callback.answer()


@router.message(ReminderTimeState.new_time)
async def reminder_set_time(message: Message, state: FSMContext, db: Database) -> None:
    try:
        reminder_time = datetime.strptime(message.text.strip(), "%H:%M").time()
    except ValueError:
        await message.answer("Неверный формат времени. Используй HH:MM")
        return

    data = await state.get_data()
    habit_id = data.get("habit_id")
    async with db.session_factory() as session:
        user = await UserRepository(session).get_by_telegram_id(message.from_user.id)
        repo = HabitRepository(session)
        habit = await repo.get_by_id(habit_id, user.id)
        if not habit:
            await message.answer("Привычка не найдена")
            await state.clear()
            return
        await repo.update_reminder_time(habit, reminder_time)

    await state.clear()
    await message.answer("Время напоминания обновлено ✅")
