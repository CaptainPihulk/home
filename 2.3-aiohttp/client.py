import asyncio
from aiohttp import ClientSession


async def main():

    async with ClientSession() as session:

        # response = await session.post('http://127.0.0.1:8080/users/register/', json={'name': 'Petya', 'password': 'Pet1234!',
        #                                                                              'email_address': 'Pet@mail.ru'})
        # print(response.status)
        # print(await response.text())
        #
        # response = await session.post('http://127.0.0.1:8080/users/login/', json={'password': 'Pet1234!',
        #                                                                           'email_address': 'Pet@mail.ru'})
        # print(response.status)
        # print(await response.text())

        # response = await session.patch('http://127.0.0.1:8080/users/15/', json={'password': 'Petya1234!'},
        #                                headers={'token': 'c3f6804f-4f8a-473c-903d-8e3c5acb93d7'})
        # print(response.status)
        # print(await response.text())

        # response = await session.get('http://127.0.0.1:8080/users/14/')
        # print(response.status)
        # print(await response.text())

        # response = await session.delete('http://127.0.0.1:8080/users/15/',
        #                                 headers={'token': 'c3f6804f-4f8a-473c-903d-8e3c5acb93d7'})
        # print(response.status)
        # print(await response.text())


        # response = await session.post('http://127.0.0.1:8080/ad/create/', json={'ad_header': 'Sale',
        #                                                                         'description': 'Car in excellent state',
        #                                                                         'owner_id': 14},
        #                               headers={'token': '7f5e8992-ae1c-483a-890e-a0130b51a3fb'})
        # print(response.status)
        # print(await response.text())

        # response = await session.get('http://127.0.0.1:8080/ad/3')
        # print(response.status)
        # print(await response.text())

        # response = await session.patch('http://127.0.0.1:8080/ad/3', json={'ad_header': 'Lenin is always alive!'},
        #                                headers={'token': '7f5e8992-ae1c-483a-890e-a0130b51a3fb'})
        # print(response.status)
        # print(await response.text())

        response = await session.delete('http://127.0.0.1:8080/ad/3',
                                        headers={'token': '7f5e8992-ae1c-483a-890e-a0130b51a3fb'})
        print(response.status)
        print(await response.text())

asyncio.run(main())
