import re
from dataclasses import dataclass, field
from typing import NewType
from uuid import UUID, uuid4

from pycommerce.core.entities.base import Entity


class InvalidUser(Exception):
    pass


Password = NewType("Password", str)
Email = NewType("Email", str)


@dataclass(frozen=True)
class User(Entity):
    name: str
    email: Email
    password: Password
    id: UUID = field(default_factory=uuid4)

    def validate(self):
        self.validate_email(self.email)
        self.validate_password(self.password)

    @staticmethod
    def validate_email(email: str) -> None:
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_pattern, email):
            raise InvalidUser(f"Invalid email address {email}")

    @staticmethod
    def validate_password(password: str) -> None:
        if not (8 <= len(password) <= 100):
            raise InvalidUser("Password size must be between 8 and 100 characters")
