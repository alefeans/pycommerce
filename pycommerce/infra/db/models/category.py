from datetime import datetime
from uuid import UUID

from sqlmodel import Field, SQLModel


class Category(SQLModel, table=True):
    id: UUID = Field(primary_key=True)
    name: str
    description: str
    created_at: datetime
