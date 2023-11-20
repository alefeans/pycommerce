from pycommerce.core.entities.user import Password
from pycommerce.infra.providers.crypto import Hasher


class UserHasher(Hasher):
    def hash(self, value: str) -> Password:
        return Password(super().hash(value))
