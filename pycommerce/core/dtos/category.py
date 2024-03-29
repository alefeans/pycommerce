from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class CreateCategory:
    name: str
    description: str


@dataclass(frozen=True)
class UpdateCategory:
    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self):
        if not self.name and not self.description:
            raise ValueError("At least one field must be provided")


@dataclass(frozen=True)
class CategoryResponse:
    id: UUID
    name: str
    description: str
    created_at: datetime
