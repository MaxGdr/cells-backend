from typing import List, Any, Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.users import User
from core.security import verify_password


class UsersCrud:
    def __init__(self, db: Session):
        self._db = db

    async def authenticate(self, email: str, password: str) -> User | None:
        user: User = (
            self._db.scalars(select(User).where(User.email == email))
        ).one_or_none()
        if not user or not verify_password(password, user.password):
            return None
        return user

    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        users: Sequence[Any] = (
            self._db.scalars(select(User).offset(skip).limit(limit))
        ).all()
        return list(users)

    async def create_user(self, user: User) -> User:
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user
