from typing import Any, Annotated, Generator
from fastapi import Depends
from pycommerce.infra.db import get_session, DBSession
from pycommerce.infra.providers.crypto import Hasher

Database = Annotated[DBSession, Depends(get_session)]


def get_repo(Repo: Any, db: Database) -> Generator[Any, None, None]:
    yield Repo(db)


def get_hashing_service():
    yield Hasher


HashingService = Annotated[Hasher, Depends(get_hashing_service)]
