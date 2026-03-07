from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.keyboards import playlists_keyboard, video_list_item_keyboard


class PlaylistStates(StatesGroup):
    waiting_for_playlist_name = State()


def setup_playlist_handlers(router: Router) -> None:
    @router.message(F.text == "🎯 Плейлисты")
    async def show_playlists(message: Message, db) -> None:
        playlists = await db.list_playlists(message.from_user.id)
        if not playlists:
            await message.answer("У вас пока нет плейлистов. Нажмите кнопку ниже, чтобы создать.")
        await message.answer("📂 Список плейлистов", reply_markup=playlists_keyboard(playlists))

    @router.callback_query(F.data == "playlist:create")
    async def create_playlist_start(callback: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(PlaylistStates.waiting_for_playlist_name)
        await callback.message.answer("Введите название нового плейлиста:")
        await callback.answer()

    @router.message(PlaylistStates.waiting_for_playlist_name)
    async def create_playlist_finish(message: Message, state: FSMContext, db) -> None:
        name = message.text.strip()
        if len(name) < 2:
            await message.answer("Название слишком короткое. Попробуйте снова.")
            return
        playlist_id = await db.create_playlist(message.from_user.id, name)
        await state.clear()
        if not playlist_id:
            await message.answer("Плейлист с таким названием уже есть.")
            return
        await message.answer(f"Плейлист «{name}» создан ✅")

    @router.callback_query(F.data.startswith("playlist:"))
    async def open_playlist(callback: CallbackQuery, db) -> None:
        _, raw_id = callback.data.split(":", 1)
        if raw_id == "create":
            await callback.answer()
            return

        playlist_id = int(raw_id)
        videos = await db.get_playlist_videos(callback.from_user.id, playlist_id)
        if not videos:
            await callback.message.answer("В этом плейлисте пока нет видео.")
            await callback.answer()
            return

        await callback.message.answer("Видео в плейлисте:")
        for video in videos:
            await callback.message.answer(
                f"{video['title']}",
                reply_markup=video_list_item_keyboard(video["id"], video["url"]),
            )
        await callback.answer()
