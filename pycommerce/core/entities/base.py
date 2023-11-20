from typing import Protocol
from uuid import UUID


class Entity(Protocol):
    id: UUID

    def __post_init__(self):
        self.validate()

    def validate(self):
        ...
