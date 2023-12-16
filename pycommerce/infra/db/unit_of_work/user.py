from pycommerce.core.protocols.user import UserRepo
from pycommerce.infra.db import DBSession
from pycommerce.infra.db.repositories.user import UserRepo as ConcreteUserRepo
from pycommerce.infra.db.unit_of_work.base import BaseUnitOfWork


class UserUnitOfWork(BaseUnitOfWork):
    def __init__(self, session: DBSession, repo: UserRepo) -> None:
        self.session = session
        self.user_repo = repo


def user_uow_factory(session: DBSession) -> UserUnitOfWork:
    return UserUnitOfWork(session, ConcreteUserRepo(session))
