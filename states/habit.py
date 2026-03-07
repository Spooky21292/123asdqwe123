from aiogram.fsm.state import State, StatesGroup


class AddHabitState(StatesGroup):
    title = State()
    description = State()
    frequency = State()
    days = State()
    reminder = State()
    reminder_time = State()


class ReminderTimeState(StatesGroup):
    choose_habit = State()
    new_time = State()
