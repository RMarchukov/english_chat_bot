from aiogram import types
from random import choice
import requests


types_of_tests = ['переклад з англійської', 'переклад з української', 'вибір з англійскої', 'вибір з української',
                  '/start']


test_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
for i in types_of_tests:
    test_keyboard.add(i)


menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
menu_keyboard.add('/settings')
menu_keyboard.add('/levels')
menu_keyboard.add('/tests')


user_words_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
user_words_menu.insert('подивитися свої слова')
user_words_menu.insert('додати слово')
user_words_menu.insert('тестування особистих слів')


group_of_words = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
group_of_words.insert('Основні слова')
group_of_words.insert('Особисті слова')


def get_levels_keyboard():
    level_filter = []
    levels_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    levels = requests.get('https://romamarchukov.pythonanywhere.com/api/levels').json()['results']
    for level in levels:
        if level['name'] == 'ir.verbs':
            levels_keyboard.add('Неправильні дієслова')
        else:
            levels_keyboard.insert(level['name'])
            level_filter.append(level['name'])
    levels_keyboard.add('Особисті слова')
    levels_keyboard.add('/start')
    return {'levels_keyboard': levels_keyboard, 'level_filter': level_filter}


def get_topics_keyboard(level=None):
    topics_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    topics = requests.get('https://romamarchukov.pythonanywhere.com/api/topics').json()['results']
    for topic in topics:
        if level == topic['level']:
            topics_keyboard.insert(topic['name'])
    topics_keyboard.add('/levels')
    topics_keyboard.add('/start')
    return {'topics_keyboard': topics_keyboard, 'topic_filter': [topic['name'] for topic in topics]}


async def get_choice_keyboard(language_of_test, words):
    choice_keyboard = types.InlineKeyboardMarkup(row_width=2)
    fake_random_words = [choice(words['results']) for _ in range(3)]
    for word in fake_random_words:
        choice_keyboard.insert(types.InlineKeyboardButton(text=word[language_of_test],
                                                          callback_data=word[language_of_test]))
    return choice_keyboard
