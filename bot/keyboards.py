from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📥 Добавить видео")],
            [KeyboardButton(text="⏳ Непросмотренные"), KeyboardButton(text="✅ Просмотренные")],
            [KeyboardButton(text="⭐ Избранные"), KeyboardButton(text="🎯 Плейлисты")],
            [KeyboardButton(text="📊 Статистика")],
        ],
        resize_keyboard=True,
    )


def video_actions_keyboard(video_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Просмотрел ✅", callback_data=f"watched:{video_id}"))
    builder.row(InlineKeyboardButton(text="⭐ В избранное", callback_data=f"favorite:{video_id}"))
    builder.row(InlineKeyboardButton(text="🧠 AI резюме", callback_data=f"summary:{video_id}"))
    builder.row(InlineKeyboardButton(text="🔔 Напомнить", callback_data=f"remind:{video_id}"))
    builder.row(InlineKeyboardButton(text="🎯 Добавить в плейлист", callback_data=f"addpl:{video_id}"))
    return builder.as_markup()


def video_list_item_keyboard(video_id: int, url: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🔗 Открыть", url=url))
    builder.row(
        InlineKeyboardButton(text="✅ Просмотрел", callback_data=f"watched:{video_id}"),
        InlineKeyboardButton(text="⭐ В избранное", callback_data=f"favorite:{video_id}"),
    )
    builder.row(
        InlineKeyboardButton(text="🧠 AI резюме", callback_data=f"summary:{video_id}"),
        InlineKeyboardButton(text="🎯 В плейлист", callback_data=f"addpl:{video_id}"),
    )
    builder.row(InlineKeyboardButton(text="🔔 Напомнить", callback_data=f"remind:{video_id}"))
    return builder.as_markup()


def watched_item_keyboard(url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔗 Открыть видео", url=url)]]
    )


def playlists_keyboard(playlists: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for playlist in playlists:
        builder.row(
            InlineKeyboardButton(
                text=f"📂 {playlist['name']}", callback_data=f"playlist:{playlist['id']}"
            )
        )
    builder.row(InlineKeyboardButton(text="➕ Создать плейлист", callback_data="playlist:create"))
    return builder.as_markup()


def add_to_playlist_keyboard(playlists: list[dict], video_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for playlist in playlists:
        builder.row(
            InlineKeyboardButton(
                text=f"🎯 {playlist['name']}",
                callback_data=f"savepl:{video_id}:{playlist['id']}",
            )
        )
    if not playlists:
        builder.row(InlineKeyboardButton(text="➕ Создать плейлист", callback_data="playlist:create"))
    return builder.as_markup()
