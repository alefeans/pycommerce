from typing import Protocol


class HashingService(Protocol):
    @staticmethod
    def hash(value: str) -> str:
        ...

    @staticmethod
    def check(value: str, hashed: str) -> bool:
        ...
