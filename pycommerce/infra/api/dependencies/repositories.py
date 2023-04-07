from functools import partial
from typing import Any, Annotated, Generator
from fastapi import Depends
from pycommerce.infra.db import get_session, DBSession
from pycommerce.infra.db.repositories import user

Database = Annotated[DBSession, Depends(get_session)]


def get_repo(Repo: Any, db: Database) -> Generator[Any, None, None]:
    yield Repo(db)


UserRepo = Annotated[user.UserRepo, Depends(partial(get_repo, user.UserRepo))]
