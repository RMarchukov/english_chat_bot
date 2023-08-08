from random import choice
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext, filters
from .user_states import ForUserHandlers
from .user_keyboards import menu_keyboard, get_levels_keyboard, get_topics_keyboard, test_keyboard,\
    get_choice_keyboard, user_words_menu, group_of_words, types_of_tests
from .user_functions import main, get_words_by_group
from aiogram.utils.exceptions import MessageIsTooLong


async def menu(message: types.Message):
    await message.answer('menu', reply_markup=menu_keyboard)
    await message.delete()


async def chose_level(message: types.Message):
    data = get_levels_keyboard()
    level_keyboard = data['levels_keyboard']
    await message.answer(text='chose level', reply_markup=level_keyboard)
    await message.delete()


async def chose_topic(message: types.Message):
    keyboard = get_topics_keyboard(message.text)
    await message.answer(text='chose topic', reply_markup=keyboard)
    await message.delete()


async def show_verbs(message: types.Message):
    verbs = await main('https://romamarchukov.pythonanywhere.com/api/verbs')
    await message.answer(f'{verbs["results"][0:33]}')
    await message.answer(f'{verbs["results"][33:66]}')
    await message.answer(f'{verbs["results"][66:99]}')
    await message.delete()


async def user_words(message: types.Message):
    await message.answer(text='choose action with your words', reply_markup=user_words_menu)
    await message.delete()


async def show_user_words(message: types.Message):
    words = await main('https://romamarchukov.pythonanywhere.com/api/user-words/')
    await message.answer(f'{words["results"][0:33]}')
    await message.answer(f'{words["results"][33:66]}')
    await message.answer(f'{words["results"][66:99]}')
    await message.delete()


async def add_user_words(message: types.Message):
    await message.answer('Напишіть слово на англійській мові')
    await ForUserHandlers.english_word.set()
    await message.delete()


async def add_english_word(message: types.Message, state: FSMContext):
    english_word = message.text.lower()
    await state.update_data(english_word=english_word)
    await message.answer('Напишіть переклад слова')
    await ForUserHandlers.ukraine_word.set()


async def add_ukraine_word(message: types.Message, state: FSMContext):
    ukraine_word = message.text.lower()
    await state.update_data(ukraine_word=ukraine_word)
    data = await state.get_data()
    request_data = {'english_word': data['english_word'], 'ukraine_word': data['ukraine_word']}
    await main('https://romamarchukov.pythonanywhere.com/api/user-words/', data=request_data)
    await message.answer(f'<b>{data.get("english_word")}  &#9824  {data.get("ukraine_word")}</b> - '
                         f'додано до списку ваших слів', parse_mode='HTML')
    await state.reset_state(with_data=False)


async def show_groups_of_words(message: types.Message):
    await message.answer(text='choose group of words', reply_markup=group_of_words)
    await message.delete()


async def show_tests(message: types.Message, state: FSMContext):
    await ForUserHandlers.words_group.set()
    await message.answer(text='choose test', reply_markup=test_keyboard)
    if message.text == 'Основні слова':
        await state.update_data(key='main_words', english_key='in_english', ukraine_key='in_ukrainian')
    elif message.text == 'Особисті слова' or message.text == 'тестування особистих слів':
        await state.update_data(key='user_words', english_key='english_word', ukraine_key='ukraine_word')
    await ForUserHandlers.word.set()
    await message.delete()


async def tests(message: types.Message, state: FSMContext):
    keys = await state.get_data()
    if message.text == '/start':
        await state.reset_state(with_data=False)
        await menu(message)
    else:
        words = await get_words_by_group(keys['key'])
        all_words = words['results']
        random_word = choice(all_words)
        if message.text == 'переклад з англійської':
            random_word_in_english = random_word.get(keys['english_key'])
            await message.answer(text=f'Перекладіть слово - <b>{random_word_in_english}</b>', parse_mode='HTML')
        elif message.text == 'переклад з української':
            random_word_in_ukrainian = random_word[keys['ukraine_key']]
            await message.answer(text=f'Перекладіть слово - <b>{random_word_in_ukrainian}</b>', parse_mode='HTML')
        elif message.text == 'вибір з англійскої':
            random_word_in_english = random_word[keys['english_key']]
            random_word_in_ukrainian = random_word[keys['ukraine_key']]
            keyboard = await get_choice_keyboard(keys['ukraine_key'], words)
            keyboard.insert(
                types.InlineKeyboardButton(text=random_word_in_ukrainian, callback_data=random_word_in_ukrainian))
            await message.answer(text=f'Перекладіть слово - <b>{random_word_in_english}</b>', parse_mode='HTML',
                                 reply_markup=keyboard)
        elif message.text == 'вибір з української':
            random_word_in_ukrainian = random_word[keys['ukraine_key']]
            random_word_in_english = random_word[keys['english_key']]
            keyboard = await get_choice_keyboard(keys['english_key'], words)
            keyboard.insert(
                types.InlineKeyboardButton(text=random_word_in_english, callback_data=random_word_in_english))
            await message.answer(text=f'Перекладіть слово - <b>{random_word_in_ukrainian}</b>', parse_mode='HTML',
                                 reply_markup=keyboard)
        await state.update_data(word=random_word)
        await ForUserHandlers.answer.set()
        await message.delete()


async def get_choice(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    ask_word = data['word']
    if callback.data == ask_word[data['english_key']]:
        await callback.answer('Відповідь правильна!', show_alert=True)
        await callback.message.answer(text=f'Слово - <b>{ask_word[data["ukraine_key"]]}</b>.\n'
                                           f'Ваша відповідь - <b>{callback.data}</b>',
                                      parse_mode='HTML')
    elif callback.data == ask_word[data['ukraine_key']]:
        await callback.answer('Відповідь правильна!', show_alert=True)
        await callback.message.answer(text=f'Слово - <b>{ask_word[data["english_key"]]}</b>.\n'
                                           f'Ваша відповідь - <b>{callback.data}</b>',
                                      parse_mode='HTML')
    else:
        await callback.answer('Відповідь не правильна', show_alert=True)
        await callback.message.answer(text=f'Правильний варіант:  <b>{ask_word[data["english_key"]]}</b>'
                                           f'  &#9824  <b>{ask_word[data["ukraine_key"]]}</b>',
                                      parse_mode='HTML')

    await state.reset_state(with_data=False)


async def get_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    ask_word = data['word']
    if message.text.lower() == ask_word[data['english_key']]:
        await message.answer(text=f'Слово - <b>{ask_word[data["ukraine_key"]]}</b>.\n'
                                  f'Ваша відповідь - <b>{message.text}</b> - правильна!', parse_mode='HTML')
    elif message.text.lower() == ask_word[data['ukraine_key']]:
        await message.answer(text=f'Слово - <b>{ask_word[data["english_key"]]}</b>.\n'
                                  f'Ваша відповідь - <b>{message.text}</b> - правильна!', parse_mode='HTML')
    else:
        await message.answer(text=f'Відповідь не правильна.\n'
                                  f'Правильний варіант:  <b>{ask_word[data["english_key"]]}</b>'
                                  f'  &#9824  <b>{ask_word[data["ukraine_key"]]}</b>',
                             parse_mode='HTML')
    await state.reset_state(with_data=False)


async def show_words(message: types.Message):
    param = message.text
    words = await main(url=f'https://romamarchukov.pythonanywhere.com/api/words/topic/{param}')
    # for word in words['results']:
    #     await message.answer(f'<b>{word["in_english"]}</b>  &#9824  <b>{word["in_ukrainian"]}</b>', parse_mode='HTML')
    try:
        await message.answer(f'норм')
        await message.answer(f'{words["results"][0:33]}')
        await message.answer(f'{words["results"][33:66]}')
        await message.answer(f'{words["results"][66:102]}')
    except MessageIsTooLong:
        await message.answer(f'если ошибка')
        await message.answer(f'{words["results"][0:10]}')
    finally:
        await message.answer(f'при любих')
        await message.answer(f'{words["results"][0:10]}')


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(menu, commands=['start', 'help'])
    dp.register_message_handler(chose_level, commands=['levels'])
    dp.register_message_handler(chose_topic, filters.Text(equals=get_levels_keyboard()['level_filter'], ignore_case=True))
    dp.register_message_handler(show_verbs, filters.Text(equals='Неправильні дієслова', ignore_case=True))
    dp.register_message_handler(user_words, filters.Text(equals='Особисті слова', ignore_case=True))
    dp.register_message_handler(show_user_words, filters.Text(equals='подивитися свої слова', ignore_case=True))
    dp.register_message_handler(add_user_words, filters.Text(equals='додати слово', ignore_case=True))
    dp.register_message_handler(add_english_word, state=ForUserHandlers.english_word)
    dp.register_message_handler(add_ukraine_word, state=ForUserHandlers.ukraine_word)
    dp.register_message_handler(show_groups_of_words, commands=['tests'])
    dp.register_message_handler(show_tests, filters.Text(equals=['особисті слова',
                                                                 'основні слова',
                                                                 'тестування особистих слів'],
                                                         ignore_case=True))
    dp.register_message_handler(tests, filters.Text(equals=types_of_tests, ignore_case=True),
                                state=ForUserHandlers.word)
    dp.register_callback_query_handler(get_choice, state=ForUserHandlers.answer)
    dp.register_message_handler(get_answer, state=ForUserHandlers.answer)
    dp.register_message_handler(show_words)
