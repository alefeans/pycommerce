from uuid import UUID
from pycommerce.core.entities.customer import (
    Customer,
    CreateCustomerDTO,
    CustomerResponse,
)
from pycommerce.core.protocols.customer import CustomerRepo, HashingService
from pycommerce.core.services.exceptions import CustomerAlreadyExists, CustomerNotFound


async def create(
    repo: CustomerRepo, hasher: HashingService, dto: CreateCustomerDTO
) -> CustomerResponse:
    if await repo.fetch_by_email(dto.email):
        raise CustomerAlreadyExists(f"Customer {dto.email} already exists")

    dto.password = await hasher.hash(dto.password)
    customer = Customer(**dto.dict())
    result = await repo.persist(customer)
    return CustomerResponse(**result.dict())


async def fetch_by_id(repo: CustomerRepo, _id: UUID) -> CustomerResponse:
    customer = await repo.fetch_by_id(_id)
    if not customer:
        raise CustomerNotFound(f"Customer {_id} not found")
    return CustomerResponse(**customer.dict())
