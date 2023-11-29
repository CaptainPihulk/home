import os
import time
import uuid
import flask_bcrypt
from app import get_app
from dotenv import load_dotenv
from errors import HttpError
from flask import request
from db import Token

load_dotenv('./env/.env')
TOKEN_TTL = int(os.getenv('TOKEN_TTL'))

app = get_app()
bcrypt = flask_bcrypt.Bcrypt(app)


def hash_password(password: str) -> str:
    return bcrypt.generate_password_hash(password.encode()).decode()


def check_password(password_hash: str, password: str,) -> bool:
    return bcrypt.check_password_hash(password_hash.encode(), password.encode())


def check_auth(session) -> Token:
    try:
        token = uuid.UUID(request.headers.get('token'))
    except (ValueError, TypeError):
        raise HttpError(403, "incorrect token")
    token = session.query(Token).get(token)

    if token is None:
        raise HttpError(403, "Empty token value")

    if time.time() - token.creation_time.timestamp() > TOKEN_TTL:
        raise HttpError(403, "token expired")

    return token
