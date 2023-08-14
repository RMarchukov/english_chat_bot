from aiogram.dispatcher import filters, FSMContext
from aiogram import types, Dispatcher
from .settings_states import UserData
from .settings_functions import get_token, delete_token, get_jwt_token, get_access_token, verify_access_token


async def site_link(message: types.Message):
    await message.answer('https://romamarchukov.pythonanywhere.com/')
    await message.delete()


async def create_tokens(message: types.Message, state: FSMContext):
    await state.update_data(type_of_token=message.text)
    await message.answer('Введіть логін: ')
    await UserData.username.set()
    await message.delete()


async def write_login(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer('Введіть пароль: ', reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
                         .add('💬Меню', '💬Налаштування'))
    await UserData.password.set()


async def write_password(message: types.Message, state: FSMContext):
    password = message.text
    await state.update_data(password=password)
    data = await state.get_data()
    username = data['username']
    password = data['password']
    auth_data = {'username': username, 'password': password}
    type_of_token = data['type_of_token']
    if type_of_token == 'Перевірити токен':
        token = await get_token(auth_data)
        if token.get('auth_token'):
            await state.update_data(token=token.get('auth_token'))
            await message.answer(f"Your token is - {token['auth_token']}")
        else:
            await message.answer(text='Невірний логін або пароль',
                                 reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
                                 .add('💬Меню', '💬Налаштування', type_of_token))

    elif type_of_token == 'Створити JWT токен':
        token = await get_jwt_token(auth_data)
        if token.get('refresh') and token.get('access'):
            await state.update_data(token=token)
            await message.answer(f"Your JWT refresh token is - {token['refresh']}")
            await message.answer(f"Your JWT access token is - {token['access']}")
        else:
            await message.answer(text='Невірний логін або пароль',
                                 reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
                                 .add('💬Меню', '💬Налаштування', type_of_token))
    await state.reset_state(with_data=False)


async def token_delete(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data.get('token'):
        result = await delete_token(data['token'])
        await message.answer(f"{data['token']} - {result}")
    else:
        await message.answer("You don`t have a token now",
                             reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                                    one_time_keyboard=True)
                             .add('Перевірити токен', '💬Меню'))
    await state.finish()


async def refresh_jwt_token(message: types.Message):
    await message.answer('Введіть refresh токен: ')
    await UserData.access_token.set()
    await message.delete()


async def show_access_token(message: types.Message, state: FSMContext):
    access_token = await get_access_token({'refresh': message.text})
    await message.answer(f"Your new access token is - {access_token['access']}")
    await state.reset_state(with_data=False)
    await message.delete()


async def verify_jwt_token(message: types.Message):
    await message.answer('Введіть access токен: ')
    await UserData.status_jwt_token.set()
    await message.delete()


async def show_jwt_status(message: types.Message, state: FSMContext):
    access_token_status = await verify_access_token({'token': message.text})
    if access_token_status == 204:
        await message.answer(f"Your JWT token is verify.")
    else:
        await message.answer(f'JWT token isn`t verify.')
    await state.reset_state(with_data=False)


def register_settings_handlers(dp: Dispatcher):
    dp.register_message_handler(site_link, filters.Text(equals='Посилання на сайт', ignore_case=True))
    dp.register_message_handler(create_tokens,
                                filters.Text(equals=['Перевірити токен', 'Створити JWT токен'], ignore_case=True))
    dp.register_message_handler(write_login, state=UserData.username)
    dp.register_message_handler(write_password, state=UserData.password)
    dp.register_message_handler(token_delete, filters.Text(equals='Видалити токен', ignore_case=True))
    dp.register_message_handler(refresh_jwt_token, filters.Text(equals='Оновити access JWT токен', ignore_case=True))
    dp.register_message_handler(show_access_token, state=UserData.access_token)
    dp.register_message_handler(verify_jwt_token, filters.Text(equals='Перевірити JWT токен', ignore_case=True))
    dp.register_message_handler(show_jwt_status, state=UserData.status_jwt_token)
