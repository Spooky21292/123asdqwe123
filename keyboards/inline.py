from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import Habit, Goal, Note


def mark_habit_keyboard(habit_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Выполнил", callback_data=f"habit_mark:{habit_id}:done")
    builder.button(text="❌ Не выполнил", callback_data=f"habit_mark:{habit_id}:missed")
    builder.button(text="⏰ Позже", callback_data=f"habit_mark:{habit_id}:later")
    builder.adjust(3)
    return builder.as_markup()


def habits_manage_keyboard(habits: list[Habit]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for habit in habits:
        status = "🟢" if habit.is_active else "⚪️"
        builder.button(text=f"{status} {habit.title}", callback_data=f"habit_view:{habit.id}")
    builder.adjust(1)
    return builder.as_markup()


def habit_actions_keyboard(habit_id: int, is_active: bool) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"habit_delete:{habit_id}")],
        [
            InlineKeyboardButton(
                text="⏸ Отключить" if is_active else "▶️ Включить",
                callback_data=f"habit_toggle:{habit_id}",
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def goals_keyboard(goals: list[Goal]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for goal in goals:
        status = "✅" if goal.is_completed else "🎯"
        builder.button(text=f"{status} {goal.title}", callback_data=f"goal_view:{goal.id}")
    builder.adjust(1)
    return builder.as_markup()


def goal_actions_keyboard(goal_id: int, completed: bool) -> InlineKeyboardMarkup:
    rows = []
    if not completed:
        rows.append([InlineKeyboardButton(text="✅ Выполнена", callback_data=f"goal_done:{goal_id}")])
    rows.append([InlineKeyboardButton(text="🗑 Удалить", callback_data=f"goal_delete:{goal_id}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def notes_keyboard(notes: list[Note]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for note in notes:
        preview = note.content[:25] + ("..." if len(note.content) > 25 else "")
        builder.button(text=f"📝 {preview}", callback_data=f"note_delete:{note.id}")
    builder.adjust(1)
    return builder.as_markup()


def reminder_habits_keyboard(habits: list[Habit]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for habit in habits:
        time_str = habit.reminder_time.strftime("%H:%M") if habit.reminder_time else "--:--"
        builder.button(text=f"{habit.title} ({time_str})", callback_data=f"remind_time:{habit.id}")
    builder.adjust(1)
    return builder.as_markup()


def stats_habits_keyboard(habits: list[Habit]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for habit in habits:
        builder.button(text=f"📈 {habit.title}", callback_data=f"habit_stats:{habit.id}")
    builder.adjust(1)
    return builder.as_markup()
