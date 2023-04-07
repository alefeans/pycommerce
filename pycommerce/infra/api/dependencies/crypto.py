from typing import Annotated, Generator
from fastapi import Depends
from passlib.context import CryptContext
from pycommerce.infra.providers.crypto import hasher
from pycommerce.core.protocols.common import HashingProvider


def get_hasher() -> Generator[CryptContext, None, None]:
    yield hasher


Hasher = Annotated[HashingProvider, Depends(get_hasher)]
