import pytest
from pydantic import EmailStr
from pycommerce.core.services import customer
from pycommerce.core.services.exceptions import CustomerAlreadyExists, CustomerNotFound
from pycommerce.core.entities.customer import Customer, CreateCustomerDTO
from pycommerce.core.protocols.customer import CustomerRepo, HashingService


@pytest.fixture
def create_customer_dto():
    return CreateCustomerDTO(
        name="Test", email=EmailStr("test@gmail.com"), password="password"
    )


@pytest.fixture
def customer_ok(create_customer_dto):
    return Customer(**create_customer_dto.dict())


@pytest.fixture
def customer_repo(async_mocker):
    return async_mocker(name="customer_repo", spec=CustomerRepo)


@pytest.fixture
def hashing_service(async_mocker):
    return async_mocker(name="hashing_service", spec=HashingService)


@pytest.mark.asyncio
async def test_if_creates_customer_successfully(
    customer_repo, hashing_service, create_customer_dto, customer_ok
):
    customer_repo.fetch_by_email.return_value = None
    customer_repo.persist.return_value = customer_ok
    hashing_service.hash.return_value = "hashed_password"

    result = await customer.create(customer_repo, hashing_service, create_customer_dto)

    customer_repo.persist.assert_called_once()
    customer_repo.fetch_by_email.assert_called_once()
    hashing_service.hash.assert_called_once()
    assert create_customer_dto.email == result.email


@pytest.mark.asyncio
async def test_if_raises_when_customer_already_exists(
    customer_repo, hashing_service, create_customer_dto, customer_ok
):
    customer_repo.fetch_by_email.return_value = customer_ok

    with pytest.raises(
        CustomerAlreadyExists, match=f"Customer {customer_ok.email} already exists"
    ):
        await customer.create(customer_repo, hashing_service, create_customer_dto)


@pytest.mark.asyncio
async def test_if_fetches_customer_by_id(customer_repo, customer_ok):
    customer_repo.fetch_by_id.return_value = customer_ok
    result = await customer.fetch_by_id(customer_repo, customer_ok.id)
    customer_repo.fetch_by_id.assert_called_once()
    assert customer_ok.id == result.id


@pytest.mark.asyncio
async def test_if_raises_when_customer_not_found(customer_repo, customer_ok):
    _id = customer_ok.id
    customer_repo.fetch_by_id.return_value = None
    with pytest.raises(CustomerNotFound, match=f"Customer {_id} not found"):
        await customer.fetch_by_id(customer_repo, _id)
    customer_repo.fetch_by_id.assert_called_once()
