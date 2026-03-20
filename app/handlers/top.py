from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.game_service import GameService

router = Router()


@router.message(Command("top"))
async def cmd_top(message: Message, session: AsyncSession) -> None:
    service = GameService(session)
    await message.answer(await service.leaderboard_text(), parse_mode="Markdown")


@router.callback_query(F.data == "menu:top")
async def cb_top(callback: CallbackQuery, session: AsyncSession) -> None:
    service = GameService(session)
    await callback.message.edit_text(await service.leaderboard_text(), parse_mode="Markdown")
    await callback.answer()
