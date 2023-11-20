from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from pycommerce.core.entities.user import Email, Password


@dataclass(frozen=True)
class CreateUser:
    name: str
    email: Email
    password: Password


@dataclass(frozen=True)
class UpdateUser:
    name: Optional[str] = None
    email: Optional[Email] = None

    def __post_init__(self):
        if not self.name and not self.email:
            raise ValueError("At least one field must be provided")


@dataclass(frozen=True)
class UserResponse:
    id: UUID
    name: str
    email: Email
