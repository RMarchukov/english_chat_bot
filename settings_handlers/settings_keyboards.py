from aiogram import types

settings_buttons = ['створити токен', 'видалити токен', 'створити JWT токен', 'оновити access JWT токен',
                    'перевірка JWT токен', 'перевірити профіль', 'посилання на сайт', '/start']


settings_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
for button in settings_buttons:
    if button == '/start':
        settings_keyboard.add(button)
    else:
        settings_keyboard.insert(button)
