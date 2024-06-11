from datetime import datetime, timedelta
from typing import List

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from core.security import create_access_token, get_password_hash
from db.users import UsersCrud
from models.users import User
from schemas.auth import TokenSchema
from schemas.users import UserSchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


class UsersManager:
    def __init__(self, session: AsyncSession):
        self._users_crud = UsersCrud(db=session)

    async def get_access_token(
        self, form_data: OAuth2PasswordRequestForm
    ) -> TokenSchema:
        user = await self._users_crud.authenticate(
            email=form_data.username, password=form_data.password
        )
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        elif not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        # TODO: Set token expiration time in settings
        access_token_expires = timedelta(minutes=30)

        return TokenSchema(
            access_token=create_access_token(
                str(user.id), expires_delta=access_token_expires
            )
        )

    async def get(self, skip: int, limit: int) -> List[UserSchema]:
        db_users: List[User] = await self._users_crud.get_users(skip=skip, limit=limit)
        return [UserSchema._from_dto(user=user) for user in db_users]

    async def create(self, user: UserSchema) -> UserSchema:
        try:
            db_user: User = await self._users_crud.create_user(
                user=User(
                    email=user.email,
                    password=get_password_hash(user.password),
                    full_name=user.full_name,
                    is_active=True,
                    created_at=datetime.now(),
                )
            )
            return UserSchema._from_dto(user=db_user)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="User already exists")
