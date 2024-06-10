from typing import Any, List

from fastapi import APIRouter

from schemas.users import (
    UserSchema,
    UsersGetResponseSchema,
    UsersCreateRequestSchema,
    UsersCreateResponseSchema,
)

from managers.users import UsersManager
from core.deps import DBSessionDep

router = APIRouter()


@router.get("/", response_model=UsersGetResponseSchema)
async def get_users(
    session: DBSessionDep,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve items.
    """

    users: List[UserSchema] = await UsersManager(session=session).get(
        skip=skip, limit=limit
    )
    print([user for user in users])

    return UsersGetResponseSchema(
        data=users,
        count=len(users),
    )


@router.post("/", response_model=UsersCreateResponseSchema)
async def create_user(
    session: DBSessionDep,
    item_request: UsersCreateRequestSchema,
) -> Any:
    """
    Create an item.
    """

    user: UserSchema = await UsersManager(session=session).create(
        user=UserSchema(
            email=item_request.email,
            password=item_request.password,
            full_name=item_request.full_name,
        )
    )
    return UsersCreateResponseSchema(data=user)
