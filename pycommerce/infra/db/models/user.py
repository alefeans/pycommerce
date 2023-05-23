from uuid import UUID
from pydantic import EmailStr
from sqlmodel import Field, SQLModel

Password = Field(..., min_length=8, max_length=100)


class User(SQLModel, table=True):
    id: UUID = Field(primary_key=True)
    name: str
    email: EmailStr
    password: str = Password
    is_admin: bool = False
