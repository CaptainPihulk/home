import os
import json
import time
import uuid
from dotenv import load_dotenv
from aiohttp import web
from sqlalchemy import select
from bcrypt import hashpw, gensalt, checkpw
from models import Token


load_dotenv('.env')
TOKEN_TTL = int(os.getenv('TOKEN_TTL'))


def hash_password(password: str) -> str:
    return hashpw(password.encode(), salt=gensalt()).decode()


def check_password(password: str, hashed_password: str) -> bool:
    return checkpw(password.encode(), hashed_password.encode())


async def check_auth(request) -> Token:
    session = request['session']
    try:
        token = uuid.UUID(request.headers.get('token'))
    except (ValueError, TypeError):
        raise web.HTTPForbidden(text=json.dumps({'status': 'error', 'message': 'Incorrect token'}),
                                content_type='application/json')

    token = await session.execute(select(Token).where(Token.id == token))
    token = token.scalars().first()

    if token is None:
        raise web.HTTPForbidden(text=json.dumps({'status': 'error', 'message': 'Empty token'}),
                                content_type='application/json')

    if time.time() - token.creation_time.timestamp() > TOKEN_TTL:
        raise web.HTTPForbidden(text=json.dumps({'status': 'error', 'message': 'Token expired"'}),
                                content_type='application/json')

    return token
