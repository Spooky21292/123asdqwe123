from __future__ import annotations

import asyncio
import re
from urllib.parse import urlparse

import yt_dlp
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from bot.ai_summary import build_video_summary
from bot.keyboards import (
    main_menu_keyboard,
    video_actions_keyboard,
    video_list_item_keyboard,
    watched_item_keyboard,
    add_to_playlist_keyboard,
)


class VideoStates(StatesGroup):
    waiting_for_link = State()


def detect_platform(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if "youtube.com" in host or "youtu.be" in host:
        return "YouTube"
    if "tiktok.com" in host:
        return "TikTok"
    return "Другое"


async def fetch_video_title(url: str) -> str | None:
    def _extract() -> str | None:
        opts = {
            "quiet": True,
            "skip_download": True,
            "no_warnings": True,
            "extract_flat": True,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get("title") if info else None

    try:
        return await asyncio.to_thread(_extract)
    except Exception:  # noqa: BLE001
        return None


def is_probable_url(text: str) -> bool:
    return bool(re.match(r"https?://", text.strip(), flags=re.IGNORECASE))


def setup_handlers(router: Router, db, settings, reminder_service) -> None:
    @router.message(CommandStart())
    async def start_command(message: Message) -> None:
        await message.answer(
            "Привет! Я помогу сохранять видео, вести плейлисты и делать AI-резюме.",
            reply_markup=main_menu_keyboard(),
        )

    @router.message(F.text == "📥 Добавить видео")
    async def add_video_prompt(message: Message, state: FSMContext) -> None:
        await state.set_state(VideoStates.waiting_for_link)
        await message.answer("Отправьте ссылку на видео (YouTube, TikTok и др.).")

    @router.message(VideoStates.waiting_for_link)
    @router.message(F.text.regexp(r"https?://"))
    async def add_video(message: Message, state: FSMContext) -> None:
        text = (message.text or "").strip()
        if not is_probable_url(text):
            await message.answer("Похоже, это не ссылка. Пришлите URL, начинающийся с http:// или https://")
            return

        platform = detect_platform(text)
        title = await fetch_video_title(text)
        final_title = title or text
        video_id = await db.add_video(message.from_user.id, text, final_title, platform)

        await state.clear()
        await message.answer(
            f"Видео добавлено.\n\nНазвание: {final_title}",
            reply_markup=video_actions_keyboard(video_id),
        )

    @router.message(F.text == "⏳ Непросмотренные")
    async def list_unwatched(message: Message) -> None:
        videos = await db.list_unwatched(message.from_user.id)
        if not videos:
            await message.answer("Список непросмотренных пуст ✅")
            return

        for video in videos:
            await message.answer(
                video["title"],
                reply_markup=video_list_item_keyboard(video["id"], video["url"]),
            )

    @router.message(F.text == "✅ Просмотренные")
    async def list_watched(message: Message) -> None:
        videos = await db.list_watched(message.from_user.id)
        if not videos:
            await message.answer("Просмотренных видео пока нет.")
            return

        for video in videos:
            watched_at = video.get("watched_at") or "—"
            await message.answer(
                f"{video['title']}\n📅 дата просмотра: {watched_at}",
                reply_markup=watched_item_keyboard(video["url"]),
            )

    @router.message(F.text == "⭐ Избранные")
    async def list_favorites(message: Message) -> None:
        videos = await db.list_favorites(message.from_user.id)
        if not videos:
            await message.answer("Избранных видео пока нет.")
            return

        for video in videos:
            await message.answer(
                video["title"],
                reply_markup=video_list_item_keyboard(video["id"], video["url"]),
            )

    @router.message(F.text == "📊 Статистика")
    async def show_stats(message: Message) -> None:
        stats = await db.get_stats(message.from_user.id)
        await message.answer(
            "📊 Ваша статистика\n\n"
            f"Всего добавлено: {stats['total']}\n"
            f"Просмотрено: {stats['watched']}\n"
            f"Непросмотрено: {stats['unwatched']}\n"
            f"Избранные: {stats['favorites']}\n"
            f"Плейлистов: {stats['playlists']}"
        )

    @router.callback_query(F.data.startswith("watched:"))
    async def mark_watched(callback: CallbackQuery) -> None:
        video_id = int(callback.data.split(":", 1)[1])
        await db.set_watched(callback.from_user.id, video_id, watched=True)
        await callback.answer("Отмечено как просмотренное ✅")

    @router.callback_query(F.data.startswith("favorite:"))
    async def toggle_favorite(callback: CallbackQuery) -> None:
        video_id = int(callback.data.split(":", 1)[1])
        favorite = await db.toggle_favorite(callback.from_user.id, video_id)
        text = "Добавлено в избранное ⭐" if favorite else "Удалено из избранного"
        await callback.answer(text)

    @router.callback_query(F.data.startswith("summary:"))
    async def ai_summary(callback: CallbackQuery) -> None:
        video_id = int(callback.data.split(":", 1)[1])
        video = await db.get_video(callback.from_user.id, video_id)
        if not video:
            await callback.answer("Видео не найдено", show_alert=True)
            return

        await callback.message.answer("Готовлю AI-резюме, это может занять до минуты... ⏳")
        summary_text = await build_video_summary(
            url=video["url"],
            api_key=settings.openai_api_key,
            model=settings.openai_model,
        )
        await callback.message.answer(f"🧠 Краткое резюме видео:\n\n{summary_text}")
        await callback.answer()

    @router.callback_query(F.data.startswith("remind:"))
    async def remind(callback: CallbackQuery) -> None:
        video_id = int(callback.data.split(":", 1)[1])
        video = await db.get_video(callback.from_user.id, video_id)
        if not video:
            await callback.answer("Видео не найдено", show_alert=True)
            return

        await reminder_service.schedule_reminder(
            user_id=callback.from_user.id,
            video_title=video["title"],
            video_url=video["url"],
            delay_minutes=60,
        )
        await callback.answer("Напоминание установлено на 60 минут 🔔")

    @router.callback_query(F.data.startswith("addpl:"))
    async def add_to_playlist_menu(callback: CallbackQuery) -> None:
        video_id = int(callback.data.split(":", 1)[1])
        playlists = await db.list_playlists(callback.from_user.id)
        await callback.message.answer(
            "Выберите плейлист:",
            reply_markup=add_to_playlist_keyboard(playlists, video_id),
        )
        await callback.answer()

    @router.callback_query(F.data.startswith("savepl:"))
    async def save_to_playlist(callback: CallbackQuery) -> None:
        _, raw_video_id, raw_playlist_id = callback.data.split(":", 2)
        saved = await db.add_video_to_playlist(
            callback.from_user.id,
            int(raw_playlist_id),
            int(raw_video_id),
        )
        if not saved:
            await callback.answer("Не удалось добавить в плейлист", show_alert=True)
            return
        await callback.answer("Видео добавлено в плейлист 🎯")
