from typing import Any

from fastapi import APIRouter

from schemas.users import (
    UserSchema,
    UsersCreateRequestSchema,
    UsersCreateResponseSchema,
)

from managers.users import UsersManager
from core.deps import DBSessionDep

router = APIRouter()


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
