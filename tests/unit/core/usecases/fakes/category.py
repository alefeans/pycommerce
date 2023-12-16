from typing import Dict, List, Optional
from uuid import UUID

from pycommerce.core.entities.category import Category
from pycommerce.core.protocols.category import CategoryRepo, CategoryUnitOfWork


class FakeCategoryRepo:
    def __init__(self) -> None:
        self.name_store: Dict[str, Category] = {}
        self.id_store: Dict[UUID, Category] = {}

    async def persist(self, category: Category) -> None:
        self.name_store[category.name] = category
        self.id_store[category.id] = category

    async def get_all(self) -> List[Category]:
        return list(self.id_store.values())

    async def get_by_id(self, _id: UUID) -> Optional[Category]:
        return self.id_store.get(_id)

    async def get_by_name(self, name: str) -> Optional[Category]:
        return self.name_store.get(name)

    async def delete(self, _id: UUID) -> bool:
        if _id not in self.id_store:
            return False
        category = self.id_store[_id]
        del self.id_store[_id]
        del self.name_store[category.name]
        return True

    async def update(self, category: Category) -> Optional[Category]:
        old = self.id_store[category.id]
        updated = Category(
            category.name or old.name,
            category.description or old.description,
            old.id,
            old.created_date,
        )
        self.id_store[old.id] = updated
        self.name_store[old.name] = updated
        return updated

    def __len__(self) -> int:
        return len(self.id_store)


class FakeCategoryUnitOfWork(CategoryUnitOfWork):
    def __init__(self, repo: CategoryRepo) -> None:
        self.category_repo = repo
        self.committed = False

    async def commit(self):
        self.committed = True

    async def rollback(self):
        pass
