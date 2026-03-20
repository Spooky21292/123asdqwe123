from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.handlers.states import CreateGameState
from app.keyboards.common import game_actions_keyboard, main_menu_keyboard, niche_keyboard, reset_confirm_keyboard
from app.services.game_service import GameService
from app.utils.messages import HELP_TEXT

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, session: AsyncSession) -> None:
    service = GameService(session)
    user = await service.register_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
    game = await service.get_active_game(user.id)
    text = (
        "Добро пожаловать в *Симулятор стартапа*!\n"
        "Здесь вы построите компанию от идеи до успеха или банкротства."
    )
    if game:
        text += "\nУ вас уже есть активная игра — можно продолжить прямо сейчас."
    else:
        text += "\nНажмите «Играть», чтобы создать свой стартап."
    await message.answer(text, reply_markup=main_menu_keyboard(), parse_mode="Markdown")


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(HELP_TEXT)


@router.message(Command("play"))
async def cmd_play(message: Message, session: AsyncSession, state: FSMContext) -> None:
    service = GameService(session)
    user = await service.register_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
    game = await service.get_active_game(user.id)
    if game:
        await message.answer("Продолжаем текущую игру.", reply_markup=game_actions_keyboard())
        return
    await state.set_state(CreateGameState.waiting_for_name)
    await message.answer("Введите название вашего стартапа.")


@router.message(CreateGameState.waiting_for_name)
async def process_startup_name(message: Message, state: FSMContext) -> None:
    await state.update_data(startup_name=message.text.strip())
    await message.answer("Выберите нишу стартапа.", reply_markup=niche_keyboard())


@router.callback_query(F.data.startswith("niche:"))
async def choose_niche(callback: CallbackQuery, session: AsyncSession, state: FSMContext) -> None:
    service = GameService(session)
    user = await service.register_user(callback.from_user.id, callback.from_user.username, callback.from_user.full_name)
    data = await state.get_data()
    startup_name = data.get("startup_name", "Мой стартап")
    niche = callback.data.split(":", 1)[1]
    from app.models.enums import StartupNiche

    game = await service.create_new_game(user.id, startup_name, StartupNiche(niche))
    await state.clear()
    await callback.message.edit_text(
        f"🚀 Стартап *{game.startup_name}* в нише *{game.startup_niche.value}* создан! Стартовый капитал: {game.money:,} ₽.",
        reply_markup=game_actions_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer()


@router.message(Command("reset"))
async def cmd_reset(message: Message) -> None:
    await message.answer("Вы уверены, что хотите начать заново?", reply_markup=reset_confirm_keyboard())


@router.callback_query(F.data == "menu:reset")
async def ask_reset(callback: CallbackQuery) -> None:
    await callback.message.answer("Подтвердите сброс активной игры.", reply_markup=reset_confirm_keyboard())
    await callback.answer()


@router.callback_query(F.data == "reset:no")
async def reset_no(callback: CallbackQuery) -> None:
    await callback.message.edit_text("Сброс отменён.", reply_markup=game_actions_keyboard())
    await callback.answer()


@router.callback_query(F.data == "reset:yes")
async def reset_yes(callback: CallbackQuery, session: AsyncSession) -> None:
    service = GameService(session)
    user = await service.register_user(callback.from_user.id, callback.from_user.username, callback.from_user.full_name)
    await service.reset_game(user.id)
    await callback.message.edit_text("Игра сброшена. Используйте /play, чтобы начать заново.", reply_markup=main_menu_keyboard())
    await callback.answer("Готово")
