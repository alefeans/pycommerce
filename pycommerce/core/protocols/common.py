from typing import Protocol


class HashingProvider(Protocol):
    @staticmethod
    def hash(value: str) -> str:
        ...

    @staticmethod
    def check(value: str, hashed: str) -> bool:
        ...
