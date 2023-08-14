import aiohttp


async def get_token(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url='https://romamarchukov.pythonanywhere.com/api/auth/token/login/',
                                data=data) as response:
            return await response.json()


async def delete_token(token):
    async with aiohttp.ClientSession() as session:
        async with session.post(url='https://romamarchukov.pythonanywhere.com/api/auth/token/logout/',
                                headers={'Authorization': f'Token {token}'}) as response:
            print(response.status)
            assert response.status == 204, 'deleted'


async def get_jwt_token(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url='https://romamarchukov.pythonanywhere.com/api/auth/jwt/create/',
                                data=data) as response:
            return await response.json()


async def get_access_token(refresh_token):
    async with aiohttp.ClientSession() as session:
        async with session.post(url='https://romamarchukov.pythonanywhere.com/api/auth/jwt/refresh/',
                                data=refresh_token) as response:
            return await response.json()


async def verify_access_token(access_token):
    async with aiohttp.ClientSession() as session:
        async with session.post(url='https://romamarchukov.pythonanywhere.com/api/auth//jwt/verify/',
                                data=access_token) as response:
            print(response.status)
            return response.status
