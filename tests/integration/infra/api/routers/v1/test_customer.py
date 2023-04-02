import pytest
from uuid import uuid4


@pytest.fixture
def customer_route():
    return "/api/v1/customers"


@pytest.fixture
def create_customer_payload():
    return {
        "name": "Test",
        "email": "test@gmail.com",
        "password": "password",
    }


async def test_get_customer_not_found(client, customer_route):
    response = await client.get(f"{customer_route}/{uuid4()}")
    data, status_code = response.json(), response.status_code
    assert status_code == 404
    assert data == {"detail": "Customer not found"}


async def test_get_customer_invalid_id(client, customer_route):
    response = await client.get(f"{customer_route}/invalid-id")
    data, status_code = response.json(), response.status_code
    assert status_code == 422
    assert data == {
        "detail": [
            {
                "loc": ["path", "customer_id"],
                "msg": "value is not a valid uuid",
                "type": "type_error.uuid",
            }
        ]
    }


async def test_create_customer_persistence(client, customer_route, create_customer_payload):
    create_response = await client.post(customer_route, json=create_customer_payload)
    created, status_code = create_response.json(), create_response.status_code
    assert status_code == 201

    get_response = await client.get(f"{customer_route}/{created['id']}")
    fetched, status_code = get_response.json(), get_response.status_code
    assert status_code == 200
    assert created["email"] == fetched["email"]


async def test_create_customer_conflict(client, customer_route, create_customer_payload):
    await client.post(customer_route, json=create_customer_payload)
    response = await client.post(customer_route, json=create_customer_payload)
    data, status_code = response.json(), response.status_code
    assert status_code == 409
    assert data == {"detail": "Customer already exists"}


async def test_delete_customer_not_found(client, customer_route):
    response = await client.delete(f"{customer_route}/{uuid4()}")
    data, status_code = response.json(), response.status_code
    assert status_code == 404
    assert data == {"detail": "Customer not found"}


async def test_delete_customer_successfully(client, customer_route, create_customer_payload):
    created_response = await client.post(customer_route, json=create_customer_payload)
    _id = created_response.json()["id"]
    delete_response = await client.delete(f"{customer_route}/{_id}")
    assert delete_response.status_code == 204
