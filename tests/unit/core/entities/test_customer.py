import pytest
from typing import Any, Dict
from pydantic import ValidationError
from pycommerce.core.entities.customer import Customer

TestData = Dict[str, Any]


@pytest.fixture
def valid_data() -> TestData:
    return {
        "name": "Test",
        "email": "test@gmail.com",
        "password": "password",
    }


@pytest.fixture
def invalid_data() -> TestData:
    return {
        "id": "",
        "name": 1,
        "email": "gmail.com",
        "password": 1,
    }


def test_if_accepts_valid_data(valid_data):
    assert Customer(**valid_data)


def test_if_automatically_generates_uuid(valid_data):
    assert Customer(**valid_data).id != Customer(**valid_data).id


def test_if_raises_when_password_has_less_than_eight_characters(valid_data):
    invalid = valid_data | {"password": "small"}
    with pytest.raises(ValidationError, match="at least 8 characters"):
        assert Customer(**invalid)


def test_if_raises_when_password_has_more_than_hundred_characters(valid_data):
    invalid = valid_data | {"password": "a" * 101}
    with pytest.raises(ValidationError, match="has at most 100 characters"):
        assert Customer(**invalid)


def test_if_raises_with_invalid_data(valid_data, invalid_data):
    with pytest.raises(ValidationError):
        Customer(**invalid_data)

    for key in valid_data.keys():
        missing = valid_data.copy()
        with pytest.raises(ValidationError, match=str(key)):
            missing.pop(key)
            Customer(**missing)


def test_if_raises_when_mutating_data(valid_data):
    customer = Customer(**valid_data)
    with pytest.raises(TypeError, match='"Customer" is immutable'):
        customer.name = "changed"
