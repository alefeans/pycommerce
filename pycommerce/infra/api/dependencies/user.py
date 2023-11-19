from typing import Annotated, AsyncGenerator

from fastapi import Depends

from pycommerce.core.protocols import user
from pycommerce.infra.db import async_session
from pycommerce.infra.db.repositories.user import UserRepo
from pycommerce.infra.db.unit_of_work.user import user_uow_factory
from pycommerce.infra.providers.user import UserHasher


async def get_user_repo() -> AsyncGenerator[user.UserRepo, None]:
    async with async_session() as session:
        yield UserRepo(session)


async def get_user_uow() -> AsyncGenerator[user.UserUnitOfWork, None]:
    async with async_session() as session:
        yield user_uow_factory(session)


Hasher = Annotated[user.UserHasher, Depends(UserHasher)]
Repo = Annotated[user.UserRepo, Depends(get_user_repo)]
UnitOfWork = Annotated[user.UserUnitOfWork, Depends(get_user_uow)]
