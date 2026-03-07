from aiogram.fsm.state import State, StatesGroup


class AddNoteState(StatesGroup):
    content = State()
