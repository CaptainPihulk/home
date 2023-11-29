import os
import json
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from aiohttp import web
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from models import Base, User, Ad, Token
from auth import check_password, hash_password, check_auth
from schema import validate, RegisterUser, LoginUser, UserData, CreateAd, AdData


load_dotenv('.env')
dsn = os.getenv('PG_DSN')
TOKEN_TTL = int(os.getenv('TOKEN_TTL'))
engine = create_async_engine(dsn)
Session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


app = web.Application()


async def orm_context(app: web.Application):
    print('START')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    print('SHUTDOWN')


@web.middleware
async def middleware(requests: web.Request, handler):
    async with Session() as session:
        requests['session'] = session
        return await handler(requests)


app.middlewares.append(middleware)
app.cleanup_ctx.append(orm_context)


async def get_user(user_id: int, session: Session):

    user = await session.get(User, user_id)
    if user is None:
        raise web.HTTPNotFound(text=json.dumps({'status': 'error', 'message': 'user not found'}),
                               content_type='application/json')
    return user


async def get_ad(ad_id: int, session: Session):

    ad = await session.get(Ad, ad_id)
    if ad is None:
        raise web.HTTPNotFound(text=json.dumps({'status': 'error', 'message': 'ad not found'}),
                               content_type='application/json')
    return ad


async def register(request):
    session = request['session']
    json_data = validate(RegisterUser, await request.json())
    json_data['password'] = hash_password(json_data['password'])
    user = User(**json_data)
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        raise web.HTTPConflict(text=json.dumps({'status': 'error', 'message': 'User already exists'}),
                               content_type='application/json')
    return web.json_response({'user_id': user.id, 'name': user.name})


class UserView(web.View):

    async def post(self):
        session = self.request['session']
        json_data = validate(LoginUser, await self.request.json())
        user = await session.execute(select(User).where(User.email_address == json_data['email_address']))
        user = user.scalars().first()
        if user is None or not check_password(json_data['password'], user.password):
            raise web.HTTPUnauthorized(text=json.dumps({'status': 'error',
                                                        'message': 'Invalid email address or password'}),
                                       content_type='application/json')
        token = Token(user=user)
        session.add(token)
        await session.commit()
        return web.json_response({'user name': user.name, 'token': str(token.id)})

    async def get(self):
        session = self.request['session']
        user_id = int(self.request.match_info['user_id'])
        user = await get_user(user_id, session)
        return web.json_response({'id': user.id, 'name': user.name})

    async def patch(self):
        user_id = int(self.request.match_info['user_id'])
        user = await get_user(user_id, self.request['session'])
        json_data = validate(UserData, await self.request.json())
        if 'password' in json_data:
            json_data['password'] = hash_password(json_data['password'])
        token = await check_auth(self.request)
        if token.user_id != user_id:
            raise web.HTTPForbidden(text=json.dumps({'status': 'error', 'message': 'Invalid user or password'}),
                                    content_type='application/json')
        for field, value in json_data.items():
            setattr(user, field, value)
        self.request['session'].add(user)
        await self.request['session'].commit()
        return web.json_response({'status': 'user information has successfully changed'})

    async def delete(self):
        user_id = int(self.request.match_info['user_id'])
        user = await get_user(user_id, self.request['session'])
        token = await check_auth(self.request)
        if token.user_id != user_id:
            raise web.HTTPForbidden(text=json.dumps({'status': 'error', 'message': 'Invalid user or password'}),
                                    content_type='application/json')
        await self.request['session'].delete(user)
        await self.request['session'].commit()
        return web.json_response({'deleting status': 'success'})


app.add_routes([web.post('/users/register/', register),
                web.post('/users/login/', UserView),
                web.get('/users/{user_id:\d+}/', UserView),
                web.patch('/users/{user_id:\d+}/', UserView),
                web.delete('/users/{user_id:\d+}/', UserView)])


class AdView(web.View):

    async def get(self):
        session = self.request['session']
        ad_id = int(self.request.match_info['ad_id'])
        ad = await get_ad(ad_id, session)
        return web.json_response({'ad id': ad.id, 'header': ad.ad_header})

    async def post(self):
        session = self.request['session']
        json_data = validate(CreateAd, await self.request.json())
        new_ad = Ad(**json_data)
        token = await check_auth(self.request)
        if token.user_id != new_ad.owner_id:
            raise web.HTTPForbidden(text=json.dumps({'status': 'error',
                                                     'message': 'You must be logged in to post ad'}),
                                    content_type='application/json')
        session.add(new_ad)
        try:
            await session.commit()
        except IntegrityError:
            raise web.HTTPConflict(text=json.dumps({'status': 'error',
                                                    'message': 'ad with these header or description already exists!'}),
                                   content_type='application/json')
        return web.json_response({'ad id': new_ad.id, 'header': new_ad.ad_header})

    async def patch(self):
        session = self.request['session']
        ad_id = int(self.request.match_info['ad_id'])
        json_data = validate(AdData, await self.request.json())
        ad = await get_ad(ad_id, session)
        token = await check_auth(self.request)
        if token.user_id != ad.owner_id:
            raise web.HTTPForbidden(text=json.dumps({'status': 'error',
                                                     'message': 'You must be owner to change the ad'}),
                                    content_type='application/json')
        for field, value in json_data.items():
            setattr(ad, field, value)
        session.add(ad)
        await session.commit()
        return web.json_response({'status': 'fields successfully changed'})

    async def delete(self):
        session = self.request['session']
        ad_id = int(self.request.match_info['ad_id'])
        ad = await get_ad(ad_id, session)
        token = await check_auth(self.request)
        if token.user_id != ad.owner_id:
            raise web.HTTPForbidden(text=json.dumps({'status': 'error',
                                                     'message': 'You must be owner to delete the ad'}),
                                    content_type='application/json')
        await session.delete(ad)
        await session.commit()
        return web.json_response({'deleting status': 'success'})


app.add_routes([web.get('/ad/{ad_id:\d+}', AdView),
                web.post('/ad/create/', AdView),
                web.patch('/ad/{ad_id:\d+}', AdView),
                web.delete('/ad/{ad_id:\d+}', AdView)])

if __name__ == '__main__':
    web.run_app(app)
