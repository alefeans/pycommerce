import pytest
from uuid import uuid4


@pytest.fixture
def create_customer_payload():
    return {
        "name": "Test",
        "email": "test@gmail.com",
        "password": "password",
    }


async def test_fetch_customer_not_found(async_test_client):
    uid = uuid4()
    async with async_test_client as client:
        response = await client.get(f"/customers/{uid}")
        data, status_code = response.json(), response.status_code
        assert status_code == 404
        assert data == {"detail": "Customer not found"}


async def test_fetch_customer_invalid_id(async_test_client):
    async with async_test_client as client:
        response = await client.get("/customers/invalid-id")
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


async def test_create_customer_persistence(async_test_client, create_customer_payload):
    async with async_test_client as client:
        response = await client.post("/customers", json=create_customer_payload)
        created, status_code = response.json(), response.status_code
        assert status_code == 201

        response = await client.get(f'/customers/{created["id"]}')
        fetched, status_code = response.json(), response.status_code
        assert status_code == 200
        assert created["email"] == fetched["email"]


async def test_create_customer_conflict(async_test_client, create_customer_payload):
    async with async_test_client as client:
        await client.post("/customers", json=create_customer_payload)
        response = await client.post("/customers", json=create_customer_payload)
        data, status_code = response.json(), response.status_code
        assert status_code == 409
        assert data == {"detail": "Customer already exists"}
