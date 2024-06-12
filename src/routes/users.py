from fastapi import APIRouter

from schemas.users import (
    UserSchema,
    UsersCreateRequestSchema,
    UserPublicSchema,
)

from managers.users import UsersManager
from core.deps import CurrentUser, DBSessionDep

router = APIRouter()


@router.post("/signup", response_model=UserPublicSchema)
async def signup(
    session: DBSessionDep,
    user_request: UsersCreateRequestSchema,
) -> UserPublicSchema:
    """
    Create new user without the need to be logged in.
    """

    user: UserPublicSchema = await UsersManager(session=session).create(
        user=UserSchema(
            email=user_request.email,
            password=user_request.password,
            full_name=user_request.full_name,
        )
    )
    return user


@router.post("/me", response_model=UserPublicSchema)
async def get_current_user(
    current_user: CurrentUser,
) -> UserPublicSchema:
    """
    Get current user.
    """

    return current_user
