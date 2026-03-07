import logging

from aiogram import Router
from aiogram.types import ErrorEvent

router = Router()
logger = logging.getLogger(__name__)


@router.error()
async def error_handler(event: ErrorEvent) -> bool:
    logger.exception("Unhandled bot error: %s", event.exception)
    if event.update.message:
        await event.update.message.answer("Упс, что-то пошло не так. Попробуй ещё раз 🙏")
    elif event.update.callback_query:
        await event.update.callback_query.answer("Ошибка, попробуй снова", show_alert=True)
    return True
