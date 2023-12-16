from uuid import uuid4

import pytest


@pytest.fixture
def category_route():
    return "/api/v1/categories"


@pytest.fixture
def create_category_payload():
    return {"name": "Test", "description": "Test description"}


@pytest.fixture
def update_category_payload():
    return {"name": "Updated", "description": "Updated description"}


async def test_get_category_not_found(client, category_route):
    response = await client.get(f"{category_route}/{uuid4()}")
    data, status_code = response.json(), response.status_code

    assert status_code == 404
    assert data == {"detail": "Category not found"}


async def test_get_category_invalid_id(client, category_route):
    response = await client.get(f"{category_route}/invalid-id")
    data, status_code = response.json(), response.status_code

    assert status_code == 422
    assert data == {
        "detail": [
            {
                "loc": ["path", "category_id"],
                "msg": "value is not a valid uuid",
                "type": "type_error.uuid",
            }
        ]
    }


async def test_get_all_categories_not_found(client, category_route):
    response = await client.get(f"{category_route}")
    data, status_code = response.json(), response.status_code

    assert status_code == 404
    assert data == {"detail": "Categories not found"}


async def test_get_all_categories(client, category_route, create_category_payload):
    create_response = await client.post(category_route, json=create_category_payload)
    created, status_code = create_response.json(), create_response.status_code

    assert status_code == 201

    get_response = await client.get(f"{category_route}")
    fetched, status_code = get_response.json(), get_response.status_code

    assert status_code == 200
    assert len(fetched) == 1
    assert fetched[0] == created


async def test_create_category_persistence(client, category_route, create_category_payload):
    create_response = await client.post(category_route, json=create_category_payload)
    created, status_code = create_response.json(), create_response.status_code

    assert status_code == 201

    get_response = await client.get(f"{category_route}/{created['id']}")
    fetched, status_code = get_response.json(), get_response.status_code

    assert status_code == 200
    assert created["name"] == fetched["name"]
    assert created["description"] == fetched["description"]
    assert created["created_at"] is not None


async def test_create_category_conflict(client, category_route, create_category_payload):
    await client.post(category_route, json=create_category_payload)
    response = await client.post(category_route, json=create_category_payload)
    data, status_code = response.json(), response.status_code

    assert status_code == 409
    assert data == {"detail": "Category already exists"}


async def test_delete_category_not_found(client, category_route):
    response = await client.delete(f"{category_route}/{uuid4()}")
    data, status_code = response.json(), response.status_code

    assert status_code == 404
    assert data == {"detail": "Category not found"}


async def test_delete_category_successfully(client, category_route, create_category_payload):
    create_response = await client.post(category_route, json=create_category_payload)
    _id = create_response.json()["id"]
    delete_response = await client.delete(f"{category_route}/{_id}")

    assert delete_response.status_code == 204


async def test_patch_category_not_found(client, category_route, update_category_payload):
    response = await client.patch(f"{category_route}/{uuid4()}", json=update_category_payload)
    data, status_code = response.json(), response.status_code

    assert status_code == 404
    assert data == {"detail": "Category not found"}


async def test_patch_all_category_data_successfully(
    client, category_route, create_category_payload, update_category_payload
):
    create_response = await client.post(category_route, json=create_category_payload)
    _id = create_response.json()["id"]
    patch_response = await client.patch(
        f"{category_route}/{_id}", json=update_category_payload
    )

    assert patch_response.status_code == 200
    assert create_response.json()["created_at"] == patch_response.json()["created_at"]
    assert patch_response.json()["name"] == update_category_payload["name"]
    assert patch_response.json()["description"] == update_category_payload["description"]


async def test_patch_partial_category_data_successfully(
    client, category_route, create_category_payload, update_category_payload
):
    create_response = await client.post(category_route, json=create_category_payload)
    _id = create_response.json()["id"]

    update_category_payload["description"] = create_category_payload["description"]
    patch_response = await client.patch(
        f"{category_route}/{_id}", json=update_category_payload
    )

    assert patch_response.status_code == 200
    assert create_response.json()["created_at"] == patch_response.json()["created_at"]
    assert patch_response.json()["name"] == update_category_payload["name"]
    assert patch_response.json()["description"] == create_category_payload["description"]

    del update_category_payload["description"]
    update_category_payload["name"] = "only name"
    patch_response = await client.patch(
        f"{category_route}/{_id}", json=update_category_payload
    )

    assert patch_response.status_code == 200
    assert create_response.json()["created_at"] == patch_response.json()["created_at"]
    assert patch_response.json()["name"] == update_category_payload["name"]
    assert patch_response.json()["description"] == create_category_payload["description"]
