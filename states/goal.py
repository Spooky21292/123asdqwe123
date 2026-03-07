from aiogram.fsm.state import State, StatesGroup


class AddGoalState(StatesGroup):
    title = State()
    description = State()
