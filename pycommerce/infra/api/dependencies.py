from typing import Any, Annotated, Generator
from fastapi import Depends
from pycommerce.infra.db import get_session, DBSession
from pycommerce.infra.providers.crypto import hasher
from pycommerce.core.protocols.common import HashingProvider

Database = Annotated[DBSession, Depends(get_session)]


def get_repo(Repo: Any, db: Database) -> Generator[Any, None, None]:
    yield Repo(db)


def get_hasher():
    yield hasher


Hasher = Annotated[HashingProvider, Depends(get_hasher)]
