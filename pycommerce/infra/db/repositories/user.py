from typing import Optional
from uuid import UUID

from sqlmodel import select

from pycommerce.core.entities.user import Email, User
from pycommerce.infra.db import DBSession
from pycommerce.infra.db.models.user import User as DBUser


class UserRepo:
    def __init__(self, session: DBSession) -> None:
        self.session = session

    async def persist(self, user: User) -> None:
        self.session.add(DBUser.from_orm(user))

    async def get_by_id(self, _id: UUID) -> Optional[User]:
        user = await self.session.get(DBUser, _id)
        return User(user.name, user.email, user.password, user.id) if user else None

    async def get_by_email(self, email: Email) -> Optional[User]:
        result = await self.session.exec(select(DBUser).where(DBUser.email == email))
        user = result.first()
        return User(user.name, user.email, user.password, user.id) if user else None

    async def delete(self, _id: UUID) -> bool:
        user = await self.session.get(DBUser, _id)
        if not user:
            return False
        await self.session.delete(user)
        return True

    async def update(self, user: User) -> Optional[User]:
        to_update = await self.session.get(DBUser, user.id)
        if not to_update:
            return None

        to_update.name = user.name
        to_update.email = user.email
        self.session.add(to_update)
        return user
