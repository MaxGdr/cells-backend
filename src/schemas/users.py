from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr
from models.users import User


class UserSchema(BaseModel):
    id: int | None = None
    email: EmailStr
    full_name: str
    password: str | None = None
    is_active: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @staticmethod
    def _from_dto(user: User):  # type: ignore
        return UserSchema(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    def _to_dto(self) -> User:
        return User(
            id=self.id,
            email=self.email,
            full_name=self.full_name,
            password=self.password,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class UsersGetRequestSchema(BaseModel):
    skip: int = 0
    limit: int = 100


class UsersGetResponseSchema(BaseModel):
    data: List[UserSchema]
    count: int


class UsersCreateRequestSchema(BaseModel):
    email: EmailStr
    full_name: str
    password: str


class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime | None = None
