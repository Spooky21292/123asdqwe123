from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.session import Database
from keyboards.inline import goal_actions_keyboard, goals_keyboard
from keyboards.reply import MAIN_MENU_TEXTS
from repositories.goals import GoalRepository
from repositories.users import UserRepository
from states.goal import AddGoalState

router = Router()


@router.message(F.text == MAIN_MENU_TEXTS["goals"])
async def goals_menu(message: Message, db: Database) -> None:
    async with db.session_factory() as session:
        user = await UserRepository(session).get_by_telegram_id(message.from_user.id)
        goals = await GoalRepository(session).get_user_goals(user.id)

    if not goals:
        await message.answer("Пока целей нет. Напиши /add_goal чтобы добавить первую 🎯")
        return
    await message.answer("Твои цели:", reply_markup=goals_keyboard(goals))


@router.message(F.text == "/add_goal")
async def add_goal_start(message: Message, state: FSMContext) -> None:
    await state.set_state(AddGoalState.title)
    await message.answer("Название цели:")


@router.message(AddGoalState.title)
async def add_goal_title(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text.strip())
    await state.set_state(AddGoalState.description)
    await message.answer("Описание (или '-' чтобы пропустить):")


@router.message(AddGoalState.description)
async def add_goal_finish(message: Message, state: FSMContext, db: Database) -> None:
    data = await state.get_data()
    description = None if message.text.strip() == "-" else message.text.strip()
    async with db.session_factory() as session:
        user = await UserRepository(session).get_by_telegram_id(message.from_user.id)
        goal = await GoalRepository(session).create(user.id, data["title"], description)
    await state.clear()
    await message.answer(f"Цель «{goal.title}» добавлена 🎯")


@router.callback_query(F.data.startswith("goal_view:"))
async def goal_view(callback: CallbackQuery, db: Database) -> None:
    goal_id = int(callback.data.split(":")[1])
    async with db.session_factory() as session:
        user = await UserRepository(session).get_by_telegram_id(callback.from_user.id)
        goal = await GoalRepository(session).get_by_id(goal_id, user.id)
    if not goal:
        await callback.answer("Цель не найдена", show_alert=True)
        return
    text = f"🎯 <b>{goal.title}</b>\n{goal.description or '-'}"
    await callback.message.answer(text, reply_markup=goal_actions_keyboard(goal.id, goal.is_completed))
    await callback.answer()


@router.callback_query(F.data.startswith("goal_done:"))
async def goal_done(callback: CallbackQuery, db: Database) -> None:
    goal_id = int(callback.data.split(":")[1])
    async with db.session_factory() as session:
        user = await UserRepository(session).get_by_telegram_id(callback.from_user.id)
        repo = GoalRepository(session)
        goal = await repo.get_by_id(goal_id, user.id)
        if goal:
            await repo.complete(goal)
    await callback.message.answer("Отличная работа! Цель отмечена как выполненная ✅")
    await callback.answer()


@router.callback_query(F.data.startswith("goal_delete:"))
async def goal_delete(callback: CallbackQuery, db: Database) -> None:
    goal_id = int(callback.data.split(":")[1])
    async with db.session_factory() as session:
        user = await UserRepository(session).get_by_telegram_id(callback.from_user.id)
        repo = GoalRepository(session)
        goal = await repo.get_by_id(goal_id, user.id)
        if goal:
            await repo.delete(goal)
    await callback.message.answer("Цель удалена 🗑")
    await callback.answer()
