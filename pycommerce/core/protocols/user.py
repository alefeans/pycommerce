from typing import Optional, Protocol
from uuid import UUID

from pycommerce.core.entities.user import Email, User
from pycommerce.core.protocols.unit_of_work import UnitOfWork


class UserRepo(Protocol):
    async def persist(self, user: User) -> None:
        ...

    async def get_by_id(self, _id: UUID) -> Optional[User]:
        ...

    async def get_by_email(self, email: Email) -> Optional[User]:
        ...

    async def delete(self, _id: UUID) -> bool:
        ...

    async def update(self, user: User) -> Optional[User]:
        ...


class UserUnitOfWork(UnitOfWork, Protocol):
    user_repo: UserRepo
