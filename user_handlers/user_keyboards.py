from aiogram import types
from random import choice
import requests


user_words_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
user_words_menu.insert('Подивитися свої слова')
user_words_menu.insert('Додати слово')
user_words_menu.insert('Тестування особистих слів')


def get_topics_keyboard(level=None):
    topics_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    topics = requests.get('https://romamarchukov.pythonanywhere.com/api/topics/').json()['results']
    for topic in topics:
        if level == topic['level']:
            topics_keyboard.insert(topic['name'])
    topics_keyboard.add('💬Рівні')
    topics_keyboard.add('💬Меню')
    return {'topics_keyboard': topics_keyboard, 'topic_filter': [topic['name'] for topic in topics]}


async def get_choice_keyboard(language_of_test, words):
    choice_keyboard = types.InlineKeyboardMarkup(row_width=2)
    fake_random_words = [choice(words['results']) for _ in range(3)]
    for word in fake_random_words:
        choice_keyboard.insert(types.InlineKeyboardButton(text=word[language_of_test],
                                                          callback_data=word[language_of_test]))
    return choice_keyboard
