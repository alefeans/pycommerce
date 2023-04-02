from uuid import UUID
from typing import Optional
from pycommerce.core.entities.customer import (
    Customer,
    CreateCustomerDTO,
    CustomerResponse,
)
from pycommerce.core.protocols.customer import CustomerRepo
from pycommerce.core.protocols.common import HashingService
from pycommerce.core.services.exceptions import CustomerAlreadyExists


async def create(
    repo: CustomerRepo, hasher: HashingService, dto: CreateCustomerDTO
) -> CustomerResponse:
    if await repo.fetch_by_email(dto.email):
        raise CustomerAlreadyExists(f"Customer {dto.email} already exists")

    dto.password = hasher.hash(dto.password)
    customer = Customer.parse_obj(dto)
    result = await repo.persist(customer)
    return CustomerResponse.parse_obj(result)


async def fetch_by_id(repo: CustomerRepo, _id: UUID) -> Optional[CustomerResponse]:
    customer = await repo.fetch_by_id(_id)
    return CustomerResponse.parse_obj(customer) if customer else None


async def delete(repo: CustomerRepo, _id: UUID) -> bool:
    return await repo.delete(_id)
