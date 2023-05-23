from uuid import UUID
from typing import Optional
from pydantic import EmailStr
from pycommerce.core.entities.user import (
    User,
    CreateUserDTO,
    UpdateUserDTO,
    UserResponse,
    Password,
)
from pycommerce.core.protocols.user import UserRepo
from pycommerce.core.protocols.common import HashingProvider
from pycommerce.core.services.exceptions import UserAlreadyExists


async def create(repo: UserRepo, hasher: HashingProvider, dto: CreateUserDTO) -> UserResponse:
    if await repo.fetch_by_email(dto.email):
        raise UserAlreadyExists(f"User {dto.email} already exists")

    dto.password = hasher.hash(dto.password)
    user = User.parse_obj(dto)
    result = await repo.persist(user)
    return UserResponse.parse_obj(result)


async def fetch_by_id(repo: UserRepo, _id: UUID) -> Optional[UserResponse]:
    user = await repo.fetch_by_id(_id)
    return UserResponse.parse_obj(user) if user else None


async def delete(repo: UserRepo, _id: UUID) -> bool:
    return await repo.delete(_id)


async def update(repo: UserRepo, _id: UUID, dto: UpdateUserDTO) -> Optional[UserResponse]:
    # FIXME
    if dto.email:
        if await repo.fetch_by_email(dto.email):
            raise UserAlreadyExists(f"Email {dto.email} is already in use")
    user = await repo.update(_id, dto)
    return UserResponse.parse_obj(user) if user else None


async def authenticate(
    repo: UserRepo, hasher: HashingProvider, email: str, password: Password
) -> Optional[UserResponse]:
    user = await repo.fetch_by_email(EmailStr(email))
    if not user:
        return None

    if not hasher.verify(password, user.password):
        return None
    return UserResponse.parse_obj(user)
