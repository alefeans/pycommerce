from pycommerce.core.protocols.category import CategoryRepo
from pycommerce.infra.db import DBSession
from pycommerce.infra.db.repositories.category import CategoryRepo as ConcreteCategoryRepo
from pycommerce.infra.db.unit_of_work.base import BaseUnitOfWork


class CategoryUnitOfWork(BaseUnitOfWork):
    def __init__(self, session: DBSession, repo: CategoryRepo) -> None:
        self.session = session
        self.category_repo = repo


def category_uow_factory(session: DBSession) -> CategoryUnitOfWork:
    return CategoryUnitOfWork(session, ConcreteCategoryRepo(session))
