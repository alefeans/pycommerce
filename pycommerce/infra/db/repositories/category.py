from typing import List, Optional
from uuid import UUID

from sqlmodel import select

from pycommerce.core.entities.category import Category
from pycommerce.infra.db import DBSession
from pycommerce.infra.db.models.category import Category as DBCategory


class CategoryRepo:
    def __init__(self, session: DBSession) -> None:
        self.session = session

    async def persist(self, category: Category) -> None:
        self.session.add(DBCategory.from_orm(category))

    async def get_all(self) -> List[Category]:
        categories = await self.session.exec(select(DBCategory))
        return [
            Category(category.name, category.description, category.id, category.created_at)
            for category in categories.all()
        ]

    async def get_by_id(self, _id: UUID) -> Optional[Category]:
        category = await self.session.get(DBCategory, _id)
        return (
            Category(category.name, category.description, category.id, category.created_at)
            if category
            else None
        )

    async def get_by_name(self, name: str) -> Optional[Category]:
        result = await self.session.exec(select(DBCategory).where(DBCategory.name == name))
        category = result.first()
        return (
            Category(category.name, category.description, category.id, category.created_at)
            if category
            else None
        )

    async def delete(self, _id: UUID) -> bool:
        category = await self.session.get(DBCategory, _id)
        if not category:
            return False
        await self.session.delete(category)
        return True

    async def update(self, category: Category) -> Optional[Category]:
        to_update = await self.session.get(DBCategory, category.id)
        if not to_update:
            return None

        to_update.name = category.name
        to_update.description = category.description
        self.session.add(to_update)
        return category
