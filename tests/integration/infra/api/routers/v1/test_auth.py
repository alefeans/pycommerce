import pytest


@pytest.fixture
def auth_route():
    return "/api/v1/auth"


@pytest.fixture
def user_route():
    return "/api/v1/users"


@pytest.fixture
def create_user_payload():
    return {
        "name": "Test",
        "email": "test@gmail.com",
        "password": "password",
    }


@pytest.fixture
def token_payload(create_user_payload):
    return {
        "username": create_user_payload["email"],
        "password": create_user_payload["password"],
    }


@pytest.fixture
def auth_token_payload(create_user_payload):
    del create_user_payload["name"]
    return create_user_payload


async def test_if_fails_to_get_access_token_for_non_existing_user(client, auth_route):
    unknown = {"username": "test@test.com", "password": "test@test"}
    response = await client.post(f"{auth_route}/token", data=unknown)

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


async def test_if_fails_to_get_access_token_for_wrong_credentials(
    client, user_route, auth_route, create_user_payload
):
    create_response = await client.post(user_route, json=create_user_payload)
    status_code = create_response.status_code

    assert status_code == 201

    payload = {"username": create_user_payload["email"], "password": "wrong"}
    response = await client.post(f"{auth_route}/token", data=payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

    payload = {"username": "wrong@test.com", "password": create_user_payload["password"]}
    response = await client.post(f"{auth_route}/token", data=payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


async def test_if_get_access_token_for_existing_user(
    client, user_route, auth_route, create_user_payload, token_payload
):
    create_response = await client.post(user_route, json=create_user_payload)

    assert create_response.status_code == 201

    response = await client.post(f"{auth_route}/token", data=token_payload)

    assert response.status_code == 200
    assert response.json()["access_token"] is not None


async def test_if_fails_to_get_authenticated_user_with_invalid_token(
    client, user_route, auth_route, create_user_payload, token_payload
):
    create_response = await client.post(user_route, json=create_user_payload)

    assert create_response.status_code == 201

    token_response = await client.post(f"{auth_route}/token", data=token_payload)

    assert token_response.status_code == 200

    headers = {"Authorization": "Bearer invalid"}
    response = await client.get(f"{auth_route}/me", headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid Token"


async def test_if_get_authenticated_user_with_valid_token(
    client, user_route, auth_route, create_user_payload, token_payload
):
    create_response = await client.post(user_route, json=create_user_payload)

    assert create_response.status_code == 201

    token_response = await client.post(f"{auth_route}/token", data=token_payload)
    token, status_code = token_response.json()["access_token"], token_response.status_code

    assert status_code == 200
    assert token is not None

    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get(f"{auth_route}/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == create_user_payload["name"]
    assert response.json()["email"] == create_user_payload["email"]
