from aiogram.dispatcher.filters.state import State, StatesGroup


class UserData(StatesGroup):
    username = State()
    password = State()
    token = State()
