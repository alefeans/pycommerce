from typing import Optional, Protocol
from uuid import UUID

from pycommerce.core.entities.user import Email, Password, User
from pycommerce.core.protocols.crypto import Hasher
from pycommerce.core.protocols.unit_of_work import UnitOfWork


class UserRepo(Protocol):
    async def persist(self, user: User) -> User:
        ...

    async def get_by_email(self, email: Email) -> Optional[User]:
        ...

    async def get_by_id(self, _id: UUID) -> Optional[User]:
        ...

    async def delete(self, _id: UUID) -> bool:
        ...

    async def update(self, user: User) -> User:
        ...


class UserUnitOfWork(UnitOfWork, Protocol):
    user_repo: UserRepo


class UserHasher(Hasher, Protocol):
    def hash(self, value: str) -> Password:
        ...
