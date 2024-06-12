from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

# from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from schemas.users import UserSchema
from sqlalchemy.orm import Session

from db.database import get_db
from core.config import settings
from models.users import User
from schemas.auth import TokenPayload


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)
TokenDep = Annotated[str, Depends(reusable_oauth2)]

DBSessionDep = Annotated[Session, Depends(get_db)]


async def get_current_user(session: DBSessionDep, token: TokenDep) -> UserSchema:
    try:
        payload = jwt.decode(
            token, settings.HASH_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return UserSchema._from_dto(user=user)


CurrentUser = Annotated[UserSchema, Depends(get_current_user)]
