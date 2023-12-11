from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from pycommerce.core.entities.base import Entity


class InvalidCategory(Exception):
    pass


@dataclass(frozen=True)
class Category(Entity):
    name: str
    description: str
    id: UUID = field(default_factory=uuid4)
    created_date: datetime = field(default_factory=datetime.now)

    def validate(self):
        self.validate_name(self.name)

    @staticmethod
    def validate_name(name: str) -> None:
        if name == "":
            raise InvalidCategory("Category name can't be empty")
        if len(name) > 100:
            raise InvalidCategory("Category name size must be less than 101 characters")
