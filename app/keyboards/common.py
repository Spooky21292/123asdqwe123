from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.models.enums import StartupNiche


def main_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🎮 Играть", callback_data="menu:play")
    builder.button(text="👤 Профиль", callback_data="menu:profile")
    builder.button(text="📊 Статистика", callback_data="menu:stats")
    builder.button(text="🏆 Топ", callback_data="menu:top")
    builder.adjust(2, 2)
    return builder.as_markup()


def niche_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for niche in StartupNiche:
        builder.button(text=niche.value, callback_data=f"niche:{niche.value}")
    builder.adjust(2)
    return builder.as_markup()


def game_actions_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = [
        ("🛠 Развивать продукт", "action:product"),
        ("📣 Запустить рекламу", "action:marketing"),
        ("👥 Нанять сотрудника", "action:hire"),
        ("🎓 Взять консультацию", "action:consult"),
        ("💼 Искать инвестора", "action:investor"),
        ("📈 Посмотреть статистику", "menu:stats"),
        ("🛍 Магазин улучшений", "menu:shop"),
        ("⏭ Следующий ход", "action:next_turn"),
        ("🔄 Рестарт игры", "menu:reset"),
    ]
    for text, data in buttons:
        builder.button(text=text, callback_data=data)
    builder.adjust(1)
    return builder.as_markup()


def shop_keyboard(upgrades: list[tuple[int, str, int, bool]]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for upgrade_id, name, cost, purchased in upgrades:
        suffix = "✅" if purchased else f"— {cost:,} ₽"
        builder.button(text=f"{name} {suffix}", callback_data=f"buy:{upgrade_id}")
    builder.button(text="⬅️ Назад", callback_data="menu:play")
    builder.adjust(1)
    return builder.as_markup()


def reset_confirm_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Да, сбросить", callback_data="reset:yes")
    builder.button(text="Нет, оставить", callback_data="reset:no")
    builder.adjust(2)
    return builder.as_markup()


def admin_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="👥 Пользователи", callback_data="admin:users")
    builder.button(text="🎮 Активные игры", callback_data="admin:games")
    builder.button(text="💸 Выдать деньги", callback_data="admin:grant")
    builder.button(text="🧹 Сбросить игру", callback_data="admin:reset")
    builder.button(text="📢 Рассылка", callback_data="admin:broadcast")
    builder.adjust(2, 2, 1)
    return builder.as_markup()
