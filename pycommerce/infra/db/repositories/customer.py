from uuid import UUID
from typing import Optional
from pydantic import EmailStr
from sqlmodel import select
from pycommerce.infra.db import DBSession
from pycommerce.core.entities.customer import Customer
from pycommerce.infra.db.models.customer import Customer as DBCustomer


class CustomerRepo:
    def __init__(self, db: DBSession) -> None:
        self.db = db

    async def fetch_by_email(self, email: EmailStr) -> Optional[Customer]:
        query = select(DBCustomer).where(DBCustomer.email == email)
        customer = await self.db.scalar(query)
        return Customer.parse_obj(customer) if customer else None

    async def fetch_by_id(self, _id: UUID) -> Optional[Customer]:
        customer = await self.db.get(DBCustomer, _id)
        return Customer.parse_obj(customer) if customer else None

    async def persist(self, customer: Customer) -> Customer:
        db_customer = DBCustomer.parse_obj(customer)
        self.db.add(db_customer)
        await self.db.commit()
        await self.db.refresh(db_customer)
        return Customer.parse_obj(db_customer)

    async def delete(self, _id: UUID) -> bool:
        customer = await self.db.get(DBCustomer, _id)
        if not customer:
            return False
        await self.db.delete(customer)
        await self.db.commit()
        return True
