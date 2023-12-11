from typing import List, Optional, Protocol
from uuid import UUID

from pycommerce.core.entities.category import Category
from pycommerce.core.protocols.unit_of_work import UnitOfWork


class CategoryRepo(Protocol):
    async def persist(self, category: Category) -> None:
        ...

    async def get_all(self) -> List[Category]:
        ...

    async def get_by_id(self, _id: UUID) -> Optional[Category]:
        ...

    async def get_by_name(self, name: str) -> Optional[Category]:
        ...

    async def delete(self, _id: UUID) -> bool:
        ...

    async def update(self, category: Category) -> Optional[Category]:
        ...


class CategoryUnitOfWork(UnitOfWork, Protocol):
    category_repo: CategoryRepo
