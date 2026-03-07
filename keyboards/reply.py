from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


MAIN_MENU_TEXTS = {
    "habits": "Мои привычки",
    "add_habit": "Добавить привычку",
    "mark_today": "Отметить сегодня",
    "stats": "Статистика",
    "goals": "Мои цели",
    "notes": "Заметки",
    "reminders": "Напоминания",
    "settings": "Настройки",
}


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=MAIN_MENU_TEXTS["habits"]), KeyboardButton(text=MAIN_MENU_TEXTS["add_habit"])],
            [KeyboardButton(text=MAIN_MENU_TEXTS["mark_today"]), KeyboardButton(text=MAIN_MENU_TEXTS["stats"])],
            [KeyboardButton(text=MAIN_MENU_TEXTS["goals"]), KeyboardButton(text=MAIN_MENU_TEXTS["notes"])],
            [KeyboardButton(text=MAIN_MENU_TEXTS["reminders"]), KeyboardButton(text=MAIN_MENU_TEXTS["settings"])],
        ],
        resize_keyboard=True,
    )
