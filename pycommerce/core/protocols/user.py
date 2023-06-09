from uuid import UUID
from typing import Protocol, Optional
from pydantic import EmailStr
from pycommerce.core.entities.user import User, UpdateUserDTO


class UserRepo(Protocol):
    async def persist(self, user: User) -> User:
        ...

    async def fetch_by_email(self, email: EmailStr) -> Optional[User]:
        ...

    async def fetch_by_id(self, _id: UUID) -> Optional[User]:
        ...

    async def delete(self, _id: UUID) -> bool:
        ...

    async def update(self, _id: UUID, dto: UpdateUserDTO) -> Optional[User]:
        ...
