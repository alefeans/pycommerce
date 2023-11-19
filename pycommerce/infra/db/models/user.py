from uuid import UUID

from sqlmodel import Field, SQLModel

from pycommerce.core.entities.user import Email, Password


class User(SQLModel, table=True):
    id: UUID = Field(primary_key=True)
    name: str
    email: Email
    password: Password
