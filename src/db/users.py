from typing import List, Any, Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User


class UsersCrud:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        users: Sequence[Any] = (
            await self._db.scalars(select(User).offset(skip).limit(limit))
        ).all()
        return list(users)

    async def create_user(self, user: User) -> User:
        self._db.add(user)
        await (
            self._db.commit()
        )  # Can be placed on manager level instead to improve commit performance
        await self._db.refresh(user)
        return user
