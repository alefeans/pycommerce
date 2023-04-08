from fastapi import APIRouter, HTTPException
from pycommerce.infra.api.dependencies.auth import (
    CurrentUser,
    Oauth2Form,
    Token,
    create_access_token,
)
from pycommerce.core.entities.user import UserResponse
from pycommerce.core.services.user import authenticate
from pycommerce.infra.api.dependencies.repositories import UserRepo
from pycommerce.infra.api.dependencies.crypto import Hasher

router = APIRouter()


@router.post(
    "/token",
    summary="Create access Token",
    responses={
        200: {"description": "User authenticated"},
        401: {"description": "User unauthorized"},
    },
    operation_id="Credentials",
)
async def token(repo: UserRepo, hasher: Hasher, form_data: Oauth2Form) -> Token:
    user = await authenticate(repo, hasher, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_access_token({"sub": f"user_id:{user.id}"})


@router.get(
    "/me",
    summary="Get authenticated User information",
    responses={
        200: {"description": "User info"},
        401: {"description": "User unauthorized"},
    },
)
async def read_users_me(current_user: CurrentUser) -> UserResponse:
    return current_user
