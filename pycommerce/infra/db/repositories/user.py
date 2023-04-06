from uuid import UUID
from typing import Optional
from pydantic import EmailStr
from sqlmodel import select
from pycommerce.infra.db import DBSession
from pycommerce.core.entities.user import User, UpdateUserDTO
from pycommerce.infra.db.models.user import User as DBUser


class UserRepo:
    def __init__(self, db: DBSession) -> None:
        self.db = db

    async def persist(self, user: User) -> User:
        db_user = DBUser.parse_obj(user)
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return User.parse_obj(db_user)

    async def fetch_by_email(self, email: EmailStr) -> Optional[User]:
        query = select(DBUser).where(DBUser.email == email)
        user = await self.db.scalar(query)
        return User.parse_obj(user) if user else None

    async def fetch_by_id(self, _id: UUID) -> Optional[User]:
        user = await self.db.get(DBUser, _id)
        return User.parse_obj(user) if user else None

    async def delete(self, _id: UUID) -> bool:
        user = await self.db.get(DBUser, _id)
        if not user:
            return False
        await self.db.delete(user)
        await self.db.commit()
        return True

    async def update(self, _id: UUID, dto: UpdateUserDTO) -> Optional[User]:
        user = await self.db.get(DBUser, _id)
        if not user:
            return None
        update_data = dto.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return User.parse_obj(user)
