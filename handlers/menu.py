from aiogram import Router
from aiogram.types import Message

from keyboards.reply import MAIN_MENU_TEXTS, main_menu_keyboard

router = Router()


@router.message(lambda m: m.text == "Меню")
async def open_menu(message: Message) -> None:
    await message.answer("Главное меню 👇", reply_markup=main_menu_keyboard())


@router.message(lambda m: m.text in MAIN_MENU_TEXTS.values())
async def menu_hint(message: Message) -> None:
    await message.answer(
        "Используй кнопки ниже. Если что-то не открывается, нажми /start для перезапуска.",
        reply_markup=main_menu_keyboard(),
    )
