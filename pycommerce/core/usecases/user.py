from typing import Optional
from uuid import UUID

from pycommerce.core.dtos.user import (
    CreateUser,
    UpdateUser,
    UserResponse,
)
from pycommerce.core.entities.user import Email, Password, User
from pycommerce.core.protocols.user import UserHasher, UserRepo, UserUnitOfWork


class UserAlreadyExists(Exception):
    pass


async def create(uow: UserUnitOfWork, hasher: UserHasher, dto: CreateUser) -> UserResponse:
    async with uow:
        if await uow.user_repo.get_by_email(dto.email):
            raise UserAlreadyExists(f"User {dto.email} already exists")

        User.validate_password(dto.password)
        user = User(dto.name, dto.email, hasher.hash(dto.password))
        await uow.user_repo.persist(user)
        return UserResponse(user.id, user.name, user.email)


async def get_by_id(repo: UserRepo, _id: UUID) -> Optional[UserResponse]:
    user = await repo.get_by_id(_id)
    if user:
        return UserResponse(user.id, user.name, user.email)


async def delete(uow: UserUnitOfWork, _id: UUID) -> bool:
    async with uow:
        return await uow.user_repo.delete(_id)


async def update(uow: UserUnitOfWork, _id: UUID, dto: UpdateUser) -> Optional[UserResponse]:
    async with uow:
        existing_user = await uow.user_repo.get_by_id(_id)

        if existing_user is None:
            return None

        updated_user = await uow.user_repo.update(
            User(
                dto.name or existing_user.name,
                dto.email or existing_user.email,
                existing_user.password,
                existing_user.id,
            )
        )

        if updated_user:
            return UserResponse(updated_user.id, updated_user.name, updated_user.email)


async def authenticate(
    repo: UserRepo, hasher: UserHasher, email: Email, password: Password
) -> Optional[UserResponse]:
    user = await repo.get_by_email(email)
    if user and hasher.verify(password, user.password):
        return UserResponse(user.id, user.name, user.email)
