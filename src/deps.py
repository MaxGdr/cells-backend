from typing import Annotated

# import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

# from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db_session

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="v1/login/access-token")


DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
# TokenDep = Annotated[str, Depends(reusable_oauth2)]


# def get_current_user(session: SessionDep, token: TokenDep) -> User:
#     try:
#         payload = jwt.decode(
#             token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
#         )
#         token_data = TokenPayload(**payload)
#     except (InvalidTokenError, ValidationError):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Could not validate credentials",
#         )
#     user = session.get(User, token_data.sub)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     if not user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return user


# CurrentUser = Annotated[User, Depends(get_current_user)]


# def get_current_active_superuser(current_user: CurrentUser) -> User:
#     if not current_user.is_superuser:
#         raise HTTPException(
#             status_code=403, detail="The user doesn't have enough privileges"
#         )
#     return current_user