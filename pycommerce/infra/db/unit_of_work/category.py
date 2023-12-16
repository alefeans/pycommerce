from pycommerce.core.protocols.category import CategoryRepo
from pycommerce.core.protocols.unit_of_work import UnitOfWork
from pycommerce.infra.db import DBSession
from pycommerce.infra.db.repositories.category import CategoryRepo as ConcreteCategoryRepo


class CategoryUnitOfWork(UnitOfWork):
    def __init__(self, session: DBSession, repo: CategoryRepo) -> None:
        self.session = session
        self.category_repo = repo

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


def category_uow_factory(session: DBSession) -> CategoryUnitOfWork:
    return CategoryUnitOfWork(session, ConcreteCategoryRepo(session))
