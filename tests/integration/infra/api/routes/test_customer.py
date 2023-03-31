from uuid import uuid4

async def test_fetch_customer_not_found(async_test_client):
    uid = uuid4()
    async with async_test_client as client:
        response = await client.get(f"/customers/{uid}")
    assert response.status_code == 404


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
