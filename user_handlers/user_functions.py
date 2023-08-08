import os
import aiohttp
from dotenv import load_dotenv


load_dotenv()
SITE_TOKEN = os.getenv('SITE_TOKEN')
PARAMS = {'Authorization': f'Token {SITE_TOKEN}'}


# async def get_topics():
#     async with aiohttp.ClientSession() as session:
#         async with session.get('https://romamarchukov.pythonanywhere.com/api/topics') as resp:
#             assert resp.status == 200
#             print(await resp.text())
#             return await resp.text()


async def main(url, data=None):
    if data:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, headers=PARAMS, data=data) as response:
                return await response.json()
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=PARAMS, data=data) as response:
                return await response.json()


async def get_words_by_group(group_of_words):
    if group_of_words == 'main_words':
        words = await main('https://romamarchukov.pythonanywhere.com/api/words/')
        return words
    elif group_of_words == 'user_words':
        words = await main('https://romamarchukov.pythonanywhere.com/api/user-words/')
        return words
