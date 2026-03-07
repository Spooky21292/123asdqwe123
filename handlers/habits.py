from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.models import FrequencyType
from database.session import Database
from keyboards.inline import habit_actions_keyboard, habits_manage_keyboard
from keyboards.reply import MAIN_MENU_TEXTS
from repositories.habits import HabitRepository
from repositories.users import UserRepository
from states.habit import AddHabitState
from utils.datetime_utils import format_days

router = Router()


@router.message(F.text == MAIN_MENU_TEXTS["add_habit"])
async def add_habit_start(message: Message, state: FSMContext) -> None:
    await state.set_state(AddHabitState.title)
    await message.answer("Как назовём привычку?")


@router.message(AddHabitState.title)
async def add_habit_title(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text.strip())
    await state.set_state(AddHabitState.description)
    await message.answer("Короткое описание (или отправь '-' чтобы пропустить):")


@router.message(AddHabitState.description)
async def add_habit_description(message: Message, state: FSMContext) -> None:
    description = None if message.text.strip() == "-" else message.text.strip()
    await state.update_data(description=description)
    await state.set_state(AddHabitState.frequency)
    await message.answer(
        "Выбери частоту:\n"
        "1 — Каждый день\n"
        "2 — По дням недели"
    )


@router.message(AddHabitState.frequency)
async def add_habit_frequency(message: Message, state: FSMContext) -> None:
    text = message.text.strip()
    if text == "1":
        await state.update_data(frequency_type=FrequencyType.DAILY.value, days_of_week=None)
        await state.set_state(AddHabitState.reminder)
        await message.answer("Включить напоминания? (да/нет)")
        return
    if text != "2":
        await message.answer("Отправь 1 или 2.")
        return

    await state.update_data(frequency_type=FrequencyType.WEEKLY.value)
    await state.set_state(AddHabitState.days)
    await message.answer("Введи дни недели цифрами через запятую (0=Пн ... 6=Вс). Например: 0,2,4")


@router.message(AddHabitState.days)
async def add_habit_days(message: Message, state: FSMContext) -> None:
    raw = message.text.replace(" ", "")
    parts = raw.split(",")
    if not parts or any(not p.isdigit() or int(p) not in range(7) for p in parts):
        await message.answer("Формат неверный. Пример: 0,2,4")
        return

    normalized = ",".join(sorted(set(parts), key=int))
    await state.update_data(days_of_week=normalized)
    await state.set_state(AddHabitState.reminder)
    await message.answer("Включить напоминания? (да/нет)")


@router.message(AddHabitState.reminder)
async def add_habit_reminder(message: Message, state: FSMContext, db: Database) -> None:
    text = message.text.strip().lower()
    if text not in {"да", "нет"}:
        await message.answer("Напиши 'да' или 'нет'.")
        return

    reminder_enabled = text == "да"
    await state.update_data(reminder_enabled=reminder_enabled)

    if reminder_enabled:
        await state.set_state(AddHabitState.reminder_time)
        await message.answer("Введи время напоминания в формате HH:MM")
        return

    await create_habit_from_state(message, state, db)


@router.message(AddHabitState.reminder_time)
async def add_habit_time(message: Message, state: FSMContext, db: Database) -> None:
    try:
        reminder_time = datetime.strptime(message.text.strip(), "%H:%M").time()
    except ValueError:
        await message.answer("Нужен формат HH:MM, например 08:30")
        return

    await state.update_data(reminder_time=reminder_time.strftime("%H:%M"))
    await create_habit_from_state(message, state, db)


async def create_habit_from_state(message: Message, state: FSMContext, db: Database | None = None) -> None:
    data = await state.get_data()
    if db is None:
        await message.answer("Произошла ошибка. Попробуй ещё раз через меню.")
        await state.clear()
        return

    async with db.session_factory() as session:
        user = await UserRepository(session).get_by_telegram_id(message.from_user.id)
        if not user:
            await message.answer("Сначала нажми /start")
            await state.clear()
            return

        reminder_time = data.get("reminder_time")
        parsed_time = datetime.strptime(reminder_time, "%H:%M").time() if reminder_time else None
        habit = await HabitRepository(session).create_habit(
            user_id=user.id,
            title=data["title"],
            description=data.get("description"),
            frequency_type=FrequencyType(data["frequency_type"]),
            days_of_week=data.get("days_of_week"),
            reminder_enabled=data.get("reminder_enabled", False),
            reminder_time=parsed_time,
        )

    await state.clear()
    await message.answer(
        f"Готово! Привычка «{habit.title}» добавлена ✅\n"
        f"Частота: {'Каждый день' if habit.frequency_type == FrequencyType.DAILY else format_days(habit.days_of_week)}"
    )


@router.message(F.text == MAIN_MENU_TEXTS["habits"])
async def list_habits(message: Message, db: Database) -> None:
    async with db.session_factory() as session:
        user = await UserRepository(session).get_by_telegram_id(message.from_user.id)
        if not user:
            await message.answer("Нажми /start")
            return
        habits = await HabitRepository(session).get_user_habits(user.id)

    if not habits:
        await message.answer("Пока нет привычек. Добавь первую через кнопку «Добавить привычку». ✨")
        return

    await message.answer("Твои привычки:", reply_markup=habits_manage_keyboard(habits))


@router.callback_query(F.data.startswith("habit_view:"))
async def habit_view(callback: CallbackQuery, db: Database) -> None:
    habit_id = int(callback.data.split(":")[1])
    async with db.session_factory() as session:
        user = await UserRepository(session).get_by_telegram_id(callback.from_user.id)
        habit = await HabitRepository(session).get_by_id(habit_id, user.id)

    if not habit:
        await callback.answer("Привычка не найдена", show_alert=True)
        return

    text = (
        f"<b>{habit.title}</b>\n"
        f"Описание: {habit.description or '-'}\n"
        f"Частота: {'Каждый день' if habit.frequency_type == FrequencyType.DAILY else format_days(habit.days_of_week)}\n"
        f"Напоминание: {'вкл' if habit.reminder_enabled else 'выкл'}"
    )
    await callback.message.answer(text, reply_markup=habit_actions_keyboard(habit.id, habit.is_active))
    await callback.answer()


@router.callback_query(F.data.startswith("habit_delete:"))
async def habit_delete(callback: CallbackQuery, db: Database) -> None:
    habit_id = int(callback.data.split(":")[1])
    async with db.session_factory() as session:
        user = await UserRepository(session).get_by_telegram_id(callback.from_user.id)
        repo = HabitRepository(session)
        habit = await repo.get_by_id(habit_id, user.id)
        if not habit:
            await callback.answer("Уже удалено", show_alert=True)
            return
        title = habit.title
        await repo.delete(habit)
    await callback.message.answer(f"Привычка «{title}» удалена 🗑")
    await callback.answer()


@router.callback_query(F.data.startswith("habit_toggle:"))
async def habit_toggle(callback: CallbackQuery, db: Database) -> None:
    habit_id = int(callback.data.split(":")[1])
    async with db.session_factory() as session:
        user = await UserRepository(session).get_by_telegram_id(callback.from_user.id)
        repo = HabitRepository(session)
        habit = await repo.get_by_id(habit_id, user.id)
        if not habit:
            await callback.answer("Привычка не найдена", show_alert=True)
            return
        habit = await repo.set_active(habit, not habit.is_active)
    await callback.message.answer(
        f"Привычка «{habit.title}» {'включена ▶️' if habit.is_active else 'отключена ⏸'}"
    )
    await callback.answer()
