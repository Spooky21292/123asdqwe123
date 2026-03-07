from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.session import Database
from keyboards.inline import notes_keyboard
from keyboards.reply import MAIN_MENU_TEXTS
from repositories.notes import NoteRepository
from repositories.users import UserRepository
from states.note import AddNoteState

router = Router()


@router.message(F.text == MAIN_MENU_TEXTS["notes"])
async def notes_menu(message: Message, db: Database) -> None:
    async with db.session_factory() as session:
        user = await UserRepository(session).get_by_telegram_id(message.from_user.id)
        notes = await NoteRepository(session).get_recent(user.id)
    if not notes:
        await message.answer("Пока заметок нет. Напиши /add_note, чтобы создать первую 📝")
        return

    lines = [f"• {note.content[:60]}" for note in notes]
    await message.answer("Последние заметки:\n" + "\n".join(lines), reply_markup=notes_keyboard(notes))


@router.message(F.text == "/add_note")
async def add_note_start(message: Message, state: FSMContext) -> None:
    await state.set_state(AddNoteState.content)
    await message.answer("Напиши заметку одним сообщением:")


@router.message(AddNoteState.content)
async def add_note_finish(message: Message, state: FSMContext, db: Database) -> None:
    content = message.text.strip()
    if not content:
        await message.answer("Пустую заметку сохранить нельзя.")
        return

    async with db.session_factory() as session:
        user = await UserRepository(session).get_by_telegram_id(message.from_user.id)
        await NoteRepository(session).create(user.id, content)

    await state.clear()
    await message.answer("Сохранил заметку 📝")


@router.callback_query(F.data.startswith("note_delete:"))
async def note_delete(callback: CallbackQuery, db: Database) -> None:
    note_id = int(callback.data.split(":")[1])
    async with db.session_factory() as session:
        user = await UserRepository(session).get_by_telegram_id(callback.from_user.id)
        repo = NoteRepository(session)
        note = await repo.get_by_id(note_id, user.id)
        if note:
            await repo.delete(note)
    await callback.answer("Заметка удалена")
    await callback.message.answer("Удалил заметку 🗑")
