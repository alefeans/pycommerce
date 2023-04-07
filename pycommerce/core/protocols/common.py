from typing import Protocol


class HashingProvider(Protocol):
    def hash(self, value: str) -> str:
        ...

    def verify(self, value: str, hashed: str) -> bool:
        ...
