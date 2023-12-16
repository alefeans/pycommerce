from typing import Annotated, AsyncGenerator

from fastapi import Depends

from pycommerce.core.protocols import category
from pycommerce.infra.db import async_session
from pycommerce.infra.db.repositories.category import CategoryRepo
from pycommerce.infra.db.unit_of_work.category import category_uow_factory


async def get_category_repo() -> AsyncGenerator[category.CategoryRepo, None]:
    async with async_session() as session:
        yield CategoryRepo(session)


async def get_category_uow() -> AsyncGenerator[category.CategoryUnitOfWork, None]:
    async with async_session() as session:
        yield category_uow_factory(session)


Repo = Annotated[category.CategoryRepo, Depends(get_category_repo)]
UnitOfWork = Annotated[category.CategoryUnitOfWork, Depends(get_category_uow)]
