from pycommerce.core.protocols.unit_of_work import UnitOfWork
from pycommerce.core.protocols.user import UserRepo
from pycommerce.infra.db import DBSession
from pycommerce.infra.db.repositories.user import UserRepo as ConcreteUserRepo


class UserUnitOfWork(UnitOfWork):
    def __init__(self, session: DBSession, repo: UserRepo) -> None:
        self.session = session
        self.user_repo = repo

    async def __aexit__(self, *args):
        super().__aexit__(*args)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


def user_uow_factory(session: DBSession) -> UserUnitOfWork:
    return UserUnitOfWork(session, ConcreteUserRepo(session))
