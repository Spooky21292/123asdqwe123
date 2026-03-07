from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from database.session import Database
from keyboards.reply import main_menu_keyboard
from repositories.users import UserRepository

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, db: Database) -> None:
    async with db.session_factory() as session:
        user_repo = UserRepository(session)
        await user_repo.get_or_create(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
        )

    text = (
        "Привет! 👋 Я бот для привычек, целей и заметок.\n\n"
        "Я помогу вести полезные привычки, отмечать прогресс каждый день, смотреть стрики и получать напоминания."
    )
    await message.answer(text, reply_markup=main_menu_keyboard())
