from aiogram.dispatcher import filters, FSMContext
from aiogram import types, Dispatcher
from .settings_keyboards import settings_keyboard
from .settings_states import UserData
from .settings_functions import create_token


async def settings(message: types.Message):
    await message.answer(text='settings menu', reply_markup=settings_keyboard)
    await message.delete()


async def site_link(message: types.Message):
    await message.answer('https://romamarchukov.pythonanywhere.com/')
    await message.delete()


async def create_main_token(message: types.Message):
    await message.answer('Введіть логін')
    await message.delete()


async def write_login(message: types.Message, state: FSMContext):
    await UserData.login.set()
    login = message.text
    await state.update_data(login=login)
    print(await state.get_data())
    await message.answer(text='Введіть пароль')
    await state.reset_state(with_data=False)
    await UserData.password.set()


async def write_password(message: types.Message, state: FSMContext):
    password = message.text
    await state.update_data(password=password)
    data = await state.get_data()
    print(data)
    token = await create_token()
    await message.answer(text=f'Your token is {token}')
    await state.reset_state(with_data=False)


# async def add_token(message: types.Message):
#     await message.answer('Enter your token from site: https://romamarchukov.pythonanywhere.com/token/')
#     await UserData.token.set()
#     await message.delete()


# async def auth_by_token(message: types.Message, state: FSMContext):
#     response = requests.get(url='https://romamarchukov.pythonanywhere.com/api/auth/users/me/',
#                             headers={'Authorization': f'Token {message.text}'})
#     username = response.json().get('username')
#     if username:
#         await state.update_data(username=username, token=message.text)
#         await message.answer(f'Your token was added.\nYour nickname at the site: {username}')
#     else:
#         await message.answer('not found this token')
#     await state.reset_state(with_data=False)
#     await message.delete()


# async def show_token(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     if data:
#         await message.answer(
#             f'Your nickname at the site is: {data.get("username")}\nYour token is: {data.get("token")}')
#     else:
#         await message.answer("You didn't do authorization")
#     await state.reset_state(with_data=False)
#     await message.delete()


def register_settings_handlers(dp: Dispatcher):
    dp.register_message_handler(settings, commands=['settings'])
    dp.register_message_handler(site_link, filters.Text(equals='посилання на сайт', ignore_case=True))
    dp.register_message_handler(create_main_token, filters.Text(equals='створити токен', ignore_case=True))
    dp.register_message_handler(write_login, state=UserData.login)
    dp.register_message_handler(write_password, state=UserData.password)
    # dp.register_message_handler(add_token, filters.Text(equals='додати токен', ignore_case=True))
    # dp.register_message_handler(auth_by_token, state=UserData.token)
    # dp.register_message_handler(show_token, filters.Text(equals='перевірити профіль', ignore_case=True))
