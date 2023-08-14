from aiogram import types, Dispatcher
from .commands_keyboards import menu_keyboard, settings_keyboard, get_levels_keyboard, group_of_words
from aiogram.dispatcher import FSMContext

async def start(message: types.Message):
    await message.answer(f'Hello {message.from_user.username}. Glad to see you!',
                         reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                                one_time_keyboard=True).add('💬Меню'))
    await message.delete()


async def menu(message: types.Message):
    await message.answer(text='Головне меню', reply_markup=menu_keyboard)
    await message.delete()


async def settings(message: types.Message):
    await message.answer(text='Налаштування', reply_markup=settings_keyboard)
    await message.delete()


async def chose_level(message: types.Message):
    data = get_levels_keyboard()
    level_keyboard = data['levels_keyboard']
    await message.answer(text='Рівні', reply_markup=level_keyboard)
    await message.delete()


async def show_groups_of_words(message: types.Message):
    await message.answer(text='choose group of words', reply_markup=group_of_words)
    await message.delete()


async def reset_states(message: types.Message, state: FSMContext):
    commands_list = ['/menu', '/start', '/levels', '/tests', '/settings']
    if message.text in commands_list:
        await state.reset_state(with_data=False)
        if message.text == '/menu':
            await menu(message)
        elif message.text == '/start':
            await start(message)
        elif message.text == '/levels':
            await chose_level(message)
        elif message.text == '/tests':
            await show_groups_of_words(message)
        elif message.text == '/settings':
            await settings(message)


def register_commands_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(menu, commands=['Меню', 'menu'], commands_prefix='💬/')
    dp.register_message_handler(settings, commands=['Налаштування', 'settings'], commands_prefix='💬/')
    dp.register_message_handler(chose_level, commands=['Рівні', 'levels'], commands_prefix='💬/')
    dp.register_message_handler(show_groups_of_words, commands=['Тести', 'tests'], commands_prefix='💬/')
    dp.register_message_handler(reset_states, state='*', commands=['menu', 'start', 'levels', 'tests', 'settings'])
