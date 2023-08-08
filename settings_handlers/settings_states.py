from aiogram.dispatcher.filters.state import State, StatesGroup


class UserData(StatesGroup):
    login = State()
    password = State()
    token = State()
