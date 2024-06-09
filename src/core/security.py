from datetime import datetime, timedelta
from typing import Any

import jwt
from passlib.context import CryptContext


ALGORITHM = "HS256"
HASH_SECRET_KEY = "ef60faf5be4074083723d9ba64af7ce69b3c392e0d588e4f44d3c8eefa2a3631"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# TODO: Move hashkey to settings
def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        payload=to_encode, key=HASH_SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bool(pwd_context.verify(plain_password, hashed_password))


def get_password_hash(password: str) -> str:
    return str(pwd_context.hash(password))
