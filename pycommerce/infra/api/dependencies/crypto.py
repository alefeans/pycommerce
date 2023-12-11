from typing import Annotated

from fastapi import Depends

from pycommerce.core.protocols.crypto import Hasher as HasherProtocol
from pycommerce.infra.providers import crypto


def get_hasher() -> crypto.Hasher:
    return crypto.Hasher()


Hasher = Annotated[HasherProtocol, Depends(get_hasher)]
