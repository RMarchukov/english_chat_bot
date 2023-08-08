from aiogram.dispatcher.filters.state import State, StatesGroup


class ForUserHandlers(StatesGroup):
    english_word = State()
    ukraine_word = State()
    words_group = State()
    word = State()
    answer = State()
