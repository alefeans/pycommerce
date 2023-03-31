from uuid import UUID
from pydantic import EmailStr
from sqlmodel import Field, SQLModel

Password = Field(..., min_length=8, max_length=100)


class Customer(SQLModel, table=True):
    id: UUID = Field(primary_key=True)
    name: str
    email: EmailStr
    password: str = Password
