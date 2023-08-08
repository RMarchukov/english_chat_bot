import aiohttp


async def create_token():
    async with aiohttp.ClientSession() as session:
        async with session.post(url='https://romamarchukov.pythonanywhere.com/api/auth/token/login/',
                                data={
                                    "password": "Ksyshka1996",
                                    "username": "Smoove"
                                },) as response:
            print(response.status)
            token_dict = await response.json()
            token = token_dict['auth_token']
            print(token)
            return token
