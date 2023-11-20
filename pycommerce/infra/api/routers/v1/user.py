from uuid import UUID

from fastapi import APIRouter, HTTPException

from pycommerce.core.dtos.user import CreateUser, UpdateUser, UserResponse
from pycommerce.core.entities.user import InvalidUser
from pycommerce.core.services import user
from pycommerce.infra.api.dependencies.user import Hasher, Repo, UnitOfWork

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
async def create(dto: CreateUser, uow: UnitOfWork, hasher: Hasher) -> UserResponse:
    try:
        return await user.create(uow, hasher, dto)
    except InvalidUser as e:
        raise HTTPException(422, detail=f"Invalid user: {e}")
    except user.UserAlreadyExists:
        raise HTTPException(409, detail="User already exists")


@router.get(
    "/{user_id}",
    summary="Get User information",
    responses={
        200: {"description": "User found"},
        404: {"description": "User not found"},
    },
)
async def get(user_id: UUID, repo: Repo) -> UserResponse:
    response = await user.get_by_id(repo, user_id)
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
async def delete(user_id: UUID, uow: UnitOfWork) -> None:
    if not await user.delete(uow, user_id):
        raise HTTPException(status_code=404, detail="User not found")


@router.patch(
    "/{user_id}",
    summary="Update User information",
    responses={
        200: {"description": "User updated"},
        404: {"description": "User not found"},
    },
)
async def patch(user_id: UUID, dto: UpdateUser, uow: UnitOfWork) -> UserResponse:
    response = await user.update(uow, user_id, dto)
    if not response:
        raise HTTPException(status_code=404, detail="User not found")
    return response
