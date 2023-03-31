from uuid import UUID
from typing import Annotated
from functools import partial
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from pycommerce.core.services import customer
from pycommerce.core.services.exceptions import CustomerAlreadyExists
from pycommerce.core.entities.customer import CustomerResponse, CreateCustomerDTO
from pycommerce.infra.db.repositories.customer import CustomerRepo
from pycommerce.infra.api.dependencies import get_repo, HashingService

router = APIRouter(prefix="/customers", tags=["Customers"])

Repo = Annotated[CustomerRepo, Depends(partial(get_repo, CustomerRepo))]


@router.post(
    "",
    status_code=201,
    summary="Create new Customer",
    responses={
        201: {"description": "Customer created successfully"},
        409: {"description": "Customer already exists"},
    },
)
async def create_customer(
    dto: CreateCustomerDTO, repo: Repo, hasher: HashingService
) -> CustomerResponse:
    try:
        response = await customer.create(repo, hasher, dto)
    except CustomerAlreadyExists:
        raise HTTPException(409, detail="Customer already exists")
    return response


@router.get(
    "/{customer_id}",
    summary="Get Customer information",
    responses={
        200: {"description": "Customer found"},
        404: {"description": "Customer not found"},
    },
)
async def health_check(customer_id: UUID, repo: Repo) -> CustomerResponse:
    response = await customer.fetch_by_id(repo, customer_id)
    if not response:
        raise HTTPException(status_code=404, detail="Customer not found")
    return response
