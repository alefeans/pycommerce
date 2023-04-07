from uuid import UUID
from operator import attrgetter
from datetime import datetime, timedelta
from typing import Any, Dict, Annotated
from pydantic import BaseModel
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pycommerce.config import get_settings
from pycommerce.core.entities.user import UserResponse
from pycommerce.core.services.user import fetch_by_id
from pycommerce.infra.api.dependencies.repositories import UserRepo

_secret_key, _expire_minutes, _algorithm = attrgetter(
    "JWT_SECRET_KEY", "JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "JWT_ALGORITHM"
)(get_settings())

CredentialsException = HTTPException(
    status_code=401,
    detail="Invalid Token",
    headers={"WWW-Authenticate": "Bearer"},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
OauthToken = Annotated[str, Depends(oauth2_scheme)]
OauthForm = Annotated[OAuth2PasswordRequestForm, Depends()]


class Token(BaseModel):
    expire: float
    access_token: str
    token_type: str = "bearer"


def decode_token(token: str) -> UUID:
    try:
        payload = jwt.decode(token, _secret_key, algorithms=[_algorithm])
    except JWTError:
        raise CredentialsException
    _, _id = str(payload.get("sub")).split(":")
    if _id is None:
        raise CredentialsException
    return UUID(_id)


def create_access_token(data: Dict[str, Any]) -> Token:
    expire = datetime.utcnow() + timedelta(minutes=_expire_minutes)
    to_encode = {**data.copy(), "exp": expire}
    access_token = jwt.encode(to_encode, _secret_key, algorithm=_algorithm)
    return Token(access_token=access_token, expire=expire.timestamp())


async def get_current_user(repo: UserRepo, token: OauthToken) -> UserResponse:
    _id = decode_token(token)
    user = await fetch_by_id(repo, _id)
    if user is None:
        raise CredentialsException
    return user


CurrentUser = Annotated[UserResponse, Depends(get_current_user)]
