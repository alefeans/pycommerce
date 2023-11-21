from fastapi import APIRouter, HTTPException

from pycommerce.core.dtos.auth import TokenResponse
from pycommerce.core.dtos.user import UserResponse
from pycommerce.core.entities.user import Email, Password
from pycommerce.core.usecases.user import authenticate
from pycommerce.infra.api.dependencies.auth import (
    CurrentUser,
    Oauth2Form,
    TokenProvider,
)
from pycommerce.infra.api.dependencies.user import Hasher, Repo

router = APIRouter()


@router.post(
    "/token",
    summary="Creates access Token",
    responses={
        200: {"description": "User authenticated"},
        401: {"description": "User unauthorized"},
    },
    operation_id="Credentials",
)
async def token(
    repo: Repo, hasher: Hasher, form_data: Oauth2Form, token_provider: TokenProvider
) -> TokenResponse:
    user = await authenticate(
        repo, hasher, Email(form_data.username), Password(form_data.password)
    )
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_provider.create_access_token({"sub": f"user_id:{user.id}"})


@router.get(
    "/me",
    summary="Gets authenticated User information",
    responses={
        200: {"description": "User info"},
        401: {"description": "User unauthorized"},
    },
)
async def get_current_user(current_user: CurrentUser) -> UserResponse:
    return current_user
