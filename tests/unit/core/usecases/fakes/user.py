from typing import Dict, List, Optional, Tuple
from uuid import UUID

from pycommerce.core.entities.user import Email, User
from pycommerce.core.protocols.user import UserRepo, UserUnitOfWork


class SpyUserHasher:
    def __init__(self) -> None:
        self.valid = True
        self.calls: List[Tuple[str, str]] = []

    def hash(self, value: str) -> str:
        self.calls.append(("hash", value))
        return "hashed_password"

    def verify(self, value: str, hashed: str) -> bool:
        self.calls.append(("verify", f"{value}, {hashed}"))
        return self.valid


class FakeUserRepo:
    def __init__(self) -> None:
        self.email_store: Dict[Email, User] = {}
        self.id_store: Dict[UUID, User] = {}

    async def persist(self, user: User) -> None:
        self.email_store[user.email] = user
        self.id_store[user.id] = user

    async def get_by_id(self, _id: UUID) -> Optional[User]:
        return self.id_store.get(_id)

    async def get_by_email(self, email: Email) -> Optional[User]:
        return self.email_store.get(email)

    async def delete(self, _id: UUID) -> bool:
        if _id not in self.id_store:
            return False
        user = self.id_store[_id]
        del self.id_store[_id]
        del self.email_store[user.email]
        return True

    async def update(self, user: User) -> Optional[User]:
        old = self.id_store[user.id]
        updated = User(
            user.name or old.name,
            user.email or old.email,
            old.password,
            old.id,
        )
        self.id_store[old.id] = updated
        self.email_store[old.email] = updated
        return updated

    def __len__(self) -> int:
        return len(self.id_store)


class FakeUserUnitOfWork(UserUnitOfWork):
    def __init__(self, repo: UserRepo) -> None:
        self.user_repo = repo
        self.committed = False

    async def commit(self):
        self.committed = True

    async def rollback(self):
        pass
