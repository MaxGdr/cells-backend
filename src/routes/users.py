from fastapi import APIRouter

from schemas.users import (
    UserSchema,
    UsersCreateRequestSchema,
    UserResponseSchema,
)

from managers.users import UsersManager
from core.deps import CurrentUser, DBSessionDep

router = APIRouter()


@router.post("/signup", response_model=UserResponseSchema)
async def signup(
    session: DBSessionDep,
    user_request: UsersCreateRequestSchema,
) -> UserResponseSchema:
    """
    Create new user without the need to be logged in.
    """

    user: UserSchema = await UsersManager(session=session).create(
        user=UserSchema(
            email=user_request.email,
            password=user_request.password,
            full_name=user_request.full_name,
        )
    )
    return UserResponseSchema(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.post("/me", response_model=UserResponseSchema)
async def get_current_user(
    current_user: CurrentUser,
) -> UserResponseSchema:
    """
    Get current user.
    """

    return UserResponseSchema(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )
