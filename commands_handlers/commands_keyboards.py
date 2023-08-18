from aiogram import types
import requests


types_of_tests = ['переклад з англійської', 'переклад з української', 'вибір з англійскої', 'вибір з української',
                  '💬Меню']


settings_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
settings_keyboard.add('Перевірити токен', 'Видалити токен', 'Створити JWT токен', 'Оновити access JWT токен',
                      'Перевірити JWT токен', 'Посилання на сайт')
settings_keyboard.add('💬Меню')


menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
menu_keyboard.add('💬Налаштування')
menu_keyboard.add('💬Рівні')
menu_keyboard.add('💬Тести')


test_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
for test in types_of_tests:
    test_keyboard.add(test)


def get_levels_keyboard():
    level_filter = []
    levels_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    levels = requests.get('https://romamarchukov.pythonanywhere.com/api/levels/').json()['results']
    for level in levels:
        if level['name'] == 'ir.verbs':
            levels_keyboard.add('Неправильні дієслова')
        else:
            levels_keyboard.insert(level['name'])
            level_filter.append(level['name'])
    levels_keyboard.add('Особисті слова')
    levels_keyboard.add('💬Меню')
    return {'levels_keyboard': levels_keyboard, 'level_filter': level_filter}


group_of_words = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
group_of_words.insert('Основні слова')
group_of_words.insert('Особисті слова')
