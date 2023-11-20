from typing import Protocol


class Hasher(Protocol):
    def hash(self, value: str) -> str:
        ...

    def verify(self, value: str, hashed: str) -> bool:
        ...
