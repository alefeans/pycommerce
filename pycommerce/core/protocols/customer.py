from uuid import UUID
from typing import Protocol, Optional
from pydantic import EmailStr
from pycommerce.core.entities.customer import Customer


class CustomerRepo(Protocol):
    async def persist(self, customer: Customer) -> Customer:
        ...

    async def fetch_by_email(self, email: EmailStr) -> Optional[Customer]:
        ...

    async def fetch_by_id(self, id: UUID) -> Optional[Customer]:
        ...

    async def delete(self, id: UUID) -> bool:
        ...
