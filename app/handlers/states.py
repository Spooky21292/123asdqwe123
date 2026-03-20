from aiogram.fsm.state import State, StatesGroup


class CreateGameState(StatesGroup):
    waiting_for_name = State()


class AdminState(StatesGroup):
    waiting_for_grant = State()
    waiting_for_reset = State()
    waiting_for_broadcast = State()
