from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.common import game_actions_keyboard, main_menu_keyboard, shop_keyboard
from app.services.game_service import GameService

router = Router()


async def _fetch_game(service: GameService, tg_user) -> tuple[object | None, object]:
    user = await service.register_user(tg_user.id, tg_user.username, tg_user.full_name)
    game = await service.get_active_game(user.id)
    return game, user


@router.message(Command("profile", "stats"))
async def cmd_profile(message: Message, session: AsyncSession) -> None:
    service = GameService(session)
    game, _ = await _fetch_game(service, message.from_user)
    if not game:
        await message.answer("У вас нет активной игры. Нажмите /play.", reply_markup=main_menu_keyboard())
        return
    await message.answer(await service.get_profile_text(game), reply_markup=game_actions_keyboard(), parse_mode="Markdown")


@router.callback_query(F.data.in_({"menu:play", "menu:profile", "menu:stats"}))
async def menu_profile(callback: CallbackQuery, session: AsyncSession) -> None:
    service = GameService(session)
    game, _ = await _fetch_game(service, callback.from_user)
    if not game:
        await callback.message.edit_text("Активная игра не найдена. Нажмите /play, чтобы начать.", reply_markup=main_menu_keyboard())
        await callback.answer()
        return
    await callback.message.edit_text(await service.get_profile_text(game), reply_markup=game_actions_keyboard(), parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data.startswith("action:"))
async def action_handler(callback: CallbackQuery, session: AsyncSession) -> None:
    service = GameService(session)
    game, _ = await _fetch_game(service, callback.from_user)
    if not game:
        await callback.message.answer("Сначала начните игру: /play")
        await callback.answer()
        return
    action = callback.data.split(":", 1)[1]
    if action == "next_turn":
        result_text, status = await service.next_turn(game)
    else:
        result_text, status = await service.do_action(game, action)
    profile_text = await service.get_profile_text(game)
    text = f"{result_text}\n\n{profile_text}"
    if status.game_over:
        text += f"\n\n*{status.outcome_title}!* {status.text}\nИтоговый счёт сохранён в базе."
        reply_markup = main_menu_keyboard()
    else:
        reply_markup = game_actions_keyboard()
    await callback.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data == "menu:shop")
async def open_shop(callback: CallbackQuery, session: AsyncSession) -> None:
    service = GameService(session)
    game, _ = await _fetch_game(service, callback.from_user)
    if not game:
        await callback.message.answer("Сначала создайте игру через /play")
        await callback.answer()
        return
    upgrades = await service.upgrades.list_upgrades()
    items = []
    for item in upgrades:
        purchased = await service.upgrades.has_upgrade(game.id, item.id)
        items.append((item.id, item.name, item.cost, purchased))
    await callback.message.edit_text("🛍 Магазин улучшений. Выберите покупку:", reply_markup=shop_keyboard(items))
    await callback.answer()


@router.callback_query(F.data.startswith("buy:"))
async def buy_upgrade(callback: CallbackQuery, session: AsyncSession) -> None:
    service = GameService(session)
    game, _ = await _fetch_game(service, callback.from_user)
    if not game:
        await callback.message.answer("Активная игра не найдена.")
        await callback.answer()
        return
    upgrade_id = int(callback.data.split(":", 1)[1])
    text = await service.buy_upgrade(game, upgrade_id)
    await callback.message.edit_text(f"{text}\n\n{await service.get_profile_text(game)}", reply_markup=game_actions_keyboard(), parse_mode="Markdown")
    await callback.answer()
