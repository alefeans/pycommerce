from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pycommerce.config import get_settings
from pycommerce.core.dtos.user import UserResponse
from pycommerce.core.usecases.user import get_by_id
from pycommerce.infra.api.dependencies.user import Repo
from pycommerce.infra.providers.jwt import InvalidToken, JWTProvider

CredentialsException = HTTPException(
    status_code=401,
    detail="Invalid Token",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_token_provider() -> JWTProvider:
    settings = get_settings()
    return JWTProvider(
        settings.JWT_SECRET_KEY,
        settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
        settings.JWT_ALGORITHM,
    )


TokenProvider = Annotated[JWTProvider, Depends(get_token_provider)]
Oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
Oauth2Token = Annotated[str, Depends(Oauth2_scheme)]
Oauth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


async def get_current_user(
    repo: Repo, token: Oauth2Token, token_provider: TokenProvider
) -> UserResponse:
    try:
        _id = token_provider.get_sub(token)
    except InvalidToken:
        raise CredentialsException

    user = await get_by_id(repo, UUID(_id))
    if user is None:
        raise CredentialsException
    return user


CurrentUser = Annotated[UserResponse, Depends(get_current_user)]
