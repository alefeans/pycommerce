from uuid import UUID
from typing import Optional
from pydantic import EmailStr
from sqlalchemy import select
from pycommerce.infra.db import DBSession
from pycommerce.core.entities.customer import Customer
from pycommerce.infra.db.models.customer import Customer as DBCustomer


class CustomerRepo:
    def __init__(self, db: DBSession) -> None:
        self.db = db

    async def persist(self, customer: Customer) -> Customer:
        db_customer = DBCustomer.parse_obj(customer)
        self.db.add(db_customer)
        await self.db.commit()
        await self.db.refresh(db_customer)
        return customer

    async def fetch_by_email(self, email: EmailStr) -> Optional[Customer]:
        query = select(DBCustomer).where(DBCustomer.email == email)
        result = await self.db.execute(query)
        customer = result.scalar()
        return Customer.parse_obj(dict(customer)) if customer else None

    async def fetch_by_id(self, _id: UUID) -> Optional[Customer]:
        query = select(DBCustomer).where(DBCustomer.id == _id)
        result = await self.db.execute(query)
        customer = result.scalar()
        return Customer.parse_obj(dict(customer)) if customer else None
