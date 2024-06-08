from typing import Annotated, Any

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm


from deps import CurrentUser, DBSessionDep
from schemas.auth import TokenSchema
from managers.users import UsersManager
from schemas.users import UserSchema

router = APIRouter()


@router.post("/access-token")
async def login_access_token(
    session: DBSessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> TokenSchema:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    token: TokenSchema = await UsersManager(session=session).get_access_token(
        form_data=form_data
    )
    return token


@router.post("/test-token", response_model=UserSchema)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user
