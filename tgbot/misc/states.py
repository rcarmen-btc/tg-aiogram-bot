from aiogram.dispatcher.filters.state import StatesGroup, State


class AddPreset(StatesGroup):
    from_enter = State()
    to_enter = State()
    enter_name = State()

