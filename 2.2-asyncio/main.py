import asyncio
import aiohttp
import datetime
from more_itertools import chunked
from models import engine, Session, Base, SwapiPeople

CHUNCK_SIZE = 10


async def get_people(session, people_id: int):
    async with session.get(f'http://swapi.dev/api/people/{people_id}') as response:
        return await response.json()


async def get_field(links: list):
    async with aiohttp.ClientSession() as session:
        if links:
            requests = [await session.get(link) for link in links]
            response = [await r.json(content_type=None) for r in requests]
            response = ", ".join([el.get('name') or el.get('title') for el in response])
            return response
        else:
            return None


async def paste_to_db(results):
    swapi_people = [SwapiPeople(name=item.get('name'),
                                birth_year=item.get('birth_year'),
                                eye_color=item.get('eye_color'),
                                films=await get_field(item.get('films')),
                                gender=item.get('gender'),
                                hair_color=item.get('hair_color'),
                                height=item.get('height'),
                                homeworld=item.get('homeworld'),
                                mass=item.get('mass'),
                                skin_color=item.get('skin_color'),
                                species=await get_field(item.get('species')),
                                starships=await get_field(item.get('starships')),
                                vehicles=await get_field(item.get('vehicles'))) for item in results]

    async with Session() as session:
        session.add_all(swapi_people)
        await session.commit()


async def main():
    start = datetime.datetime.now()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session = aiohttp.ClientSession()
    coros = (get_people(session, i) for i in range(1, 83))
    for coros_chunk in chunked(coros, CHUNCK_SIZE):
        results = await asyncio.gather(*coros_chunk)
        asyncio.create_task(paste_to_db(results))

    await session.close()
    set_tasks = asyncio.all_tasks()
    for task in set_tasks:
        if task != asyncio.current_task():
            await task
    print(datetime.datetime.now()-start)

asyncio.get_event_loop().run_until_complete(main())
