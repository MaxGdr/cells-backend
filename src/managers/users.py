from datetime import datetime
from typing import List

from fastapi import HTTPException
from db.users import UsersCrud
from models.users import User
from schemas.users import UserSchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


class UsersManager:
    def __init__(self, session: AsyncSession):
        self._users_crud = UsersCrud(db=session)

    async def get(self, skip: int, limit: int) -> List[UserSchema]:
        db_users: List[User] = await self._users_crud.get_users(skip=skip, limit=limit)
        return [UserSchema._from_dto(user=user) for user in db_users]

    async def create(self, user: UserSchema) -> UserSchema:
        try:
            db_user: User = await self._users_crud.create_user(
                user=User(
                    email=user.email,
                    password=user.password,
                    full_name=user.full_name,
                    is_active=True,
                    created_at=datetime.now(),
                    items=[],
                )
            )
            return db_user
        except IntegrityError:
            raise HTTPException(status_code=400, detail="User already exists")
