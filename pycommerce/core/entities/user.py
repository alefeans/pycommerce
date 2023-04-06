from uuid import UUID, uuid4
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


ID = Field(default_factory=uuid4)
Password = Field(..., min_length=8, max_length=100)


class User(BaseModel):
    id: UUID = ID
    name: str
    email: EmailStr
    password: str = Password

    class Config:
        allow_mutation = False
        orm_mode = True


class CreateUserDTO(BaseModel):
    name: str
    email: EmailStr
    password: str = Password


class UpdateUserDTO(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]


class UserResponse(BaseModel):
    id: UUID = ID
    name: str
    email: EmailStr

    class Config:
        allow_mutation = False
