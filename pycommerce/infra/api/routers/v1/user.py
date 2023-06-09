from uuid import UUID
from fastapi import APIRouter, HTTPException
from pycommerce.core.services import user
from pycommerce.core.services.exceptions import UserAlreadyExists
from pycommerce.core.entities.user import UserResponse, CreateUserDTO, UpdateUserDTO
from pycommerce.infra.api.dependencies.repositories import UserRepo
from pycommerce.infra.api.dependencies.crypto import Hasher

router = APIRouter()


@router.post(
    "",
    status_code=201,
    summary="Create new User",
    responses={
        201: {"description": "User created successfully"},
        409: {"description": "User already exists"},
    },
)
async def create(dto: CreateUserDTO, repo: UserRepo, hasher: Hasher) -> UserResponse:
    try:
        response = await user.create(repo, hasher, dto)
    except UserAlreadyExists:
        raise HTTPException(409, detail="User already exists")
    return response


@router.get(
    "/{user_id}",
    summary="Get User information",
    responses={
        200: {"description": "User found"},
        404: {"description": "User not found"},
    },
)
async def get(user_id: UUID, repo: UserRepo) -> UserResponse:
    response = await user.fetch_by_id(repo, user_id)
    if not response:
        raise HTTPException(status_code=404, detail="User not found")
    return response


@router.delete(
    "/{user_id}",
    status_code=204,
    summary="Delete User",
    responses={
        204: {"description": "User deleted successfully"},
        404: {"description": "User not found"},
    },
)
async def delete(user_id: UUID, repo: UserRepo) -> None:
    if not await user.delete(repo, user_id):
        raise HTTPException(status_code=404, detail="User not found")


@router.patch(
    "/{user_id}",
    summary="Update User information",
    responses={
        200: {"description": "User updated"},
        404: {"description": "User not found"},
    },
)
async def patch(user_id: UUID, dto: UpdateUserDTO, repo: UserRepo) -> UserResponse:
    response = await user.update(repo, user_id, dto)
    if not response:
        raise HTTPException(status_code=404, detail="User not found")
    return response
