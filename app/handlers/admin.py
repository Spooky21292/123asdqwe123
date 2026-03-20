from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database.repositories import GameRepository, UserRepository
from app.handlers.states import AdminState
from app.keyboards.common import admin_keyboard
from app.models import User
from app.services.game_service import GameService

router = Router()
settings = get_settings()


def is_admin(user_id: int) -> bool:
    return user_id == settings.admin_id


@router.message(Command("admin"))
async def cmd_admin(message: Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("Команда доступна только администратору.")
        return
    await message.answer("Админ-панель", reply_markup=admin_keyboard())


@router.callback_query(F.data.startswith("admin:"))
async def admin_actions(callback: CallbackQuery, session: AsyncSession, state: FSMContext, bot) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return
    action = callback.data.split(":", 1)[1]
    users_repo = UserRepository(session)
    games_repo = GameRepository(session)
    if action == "users":
        await callback.message.answer(f"Пользователей: {await users_repo.count_users()}")
    elif action == "games":
        await callback.message.answer(f"Активных игр: {await games_repo.count_active_games()}")
    elif action == "grant":
        await state.set_state(AdminState.waiting_for_grant)
        await callback.message.answer("Отправьте: user_telegram_id сумма")
    elif action == "reset":
        await state.set_state(AdminState.waiting_for_reset)
        await callback.message.answer("Отправьте telegram_id пользователя для сброса игры")
    elif action == "broadcast":
        await state.set_state(AdminState.waiting_for_broadcast)
        await callback.message.answer("Отправьте текст рассылки")
    await callback.answer()


@router.message(AdminState.waiting_for_grant)
async def admin_grant(message: Message, session: AsyncSession, state: FSMContext) -> None:
    if not is_admin(message.from_user.id):
        return
    try:
        tg_id_raw, amount_raw = message.text.split(maxsplit=1)
        tg_id, amount = int(tg_id_raw), int(amount_raw)
    except ValueError:
        await message.answer("Неверный формат. Используйте: user_telegram_id сумма")
        return
    users = UserRepository(session)
    user = await users.get_by_telegram_id(tg_id)
    if not user:
        await message.answer("Пользователь не найден.")
        return
    service = GameService(session)
    game = await service.get_active_game(user.id)
    if not game:
        await message.answer("У пользователя нет активной игры.")
        return
    game.money += amount
    await service.games.save(game)
    await state.clear()
    await message.answer(f"Выдано {amount:,} ₽ пользователю {tg_id}.")


@router.message(AdminState.waiting_for_reset)
async def admin_reset(message: Message, session: AsyncSession, state: FSMContext) -> None:
    if not is_admin(message.from_user.id):
        return
    try:
        tg_id = int(message.text.strip())
    except ValueError:
        await message.answer("Нужен целочисленный telegram_id.")
        return
    users = UserRepository(session)
    user = await users.get_by_telegram_id(tg_id)
    if not user:
        await message.answer("Пользователь не найден.")
        return
    service = GameService(session)
    await service.reset_game(user.id)
    await state.clear()
    await message.answer("Игра пользователя сброшена.")


@router.message(AdminState.waiting_for_broadcast)
async def admin_broadcast(message: Message, session: AsyncSession, state: FSMContext, bot) -> None:
    if not is_admin(message.from_user.id):
        return
    text = message.text.strip()
    result = await session.execute(select(User))
    users = list(result.scalars().all())
    delivered = 0
    for user in users:
        try:
            await bot.send_message(user.telegram_id, f"📢 Сообщение от администратора:\n\n{text}")
            delivered += 1
        except Exception:
            continue
    await state.clear()
    await message.answer(f"Рассылка завершена. Доставлено: {delivered}")
