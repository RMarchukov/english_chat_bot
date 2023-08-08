import aiohttp


async def create_token(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url='https://romamarchukov.pythonanywhere.com/api/auth/token/login/',
                                data=data) as response:
            print(response.status)
            token_dict = await response.json()
            print(token_dict)
            # token = token_dict['auth_token']
            # print(token)
            return token_dict
