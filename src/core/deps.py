from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

# from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db_session
from core.security import HASH_SECRET_KEY, ALGORITHM
from models.users import User
from schemas.auth import TokenPayload


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="v1/login/access-token")
TokenDep = Annotated[str, Depends(reusable_oauth2)]

DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]


async def get_current_user(session: DBSessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(token, HASH_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )
    user = await session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
