import pytest
from typing import Any, Dict
from pydantic import ValidationError
from pycommerce.core.entities.user import User

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
    assert User.parse_obj(valid_data)


def test_if_automatically_generates_uuid(valid_data):
    assert User.parse_obj(valid_data).id != User.parse_obj(valid_data).id


def test_if_raises_when_password_has_less_than_eight_characters(valid_data):
    invalid = valid_data | {"password": "small"}
    with pytest.raises(ValidationError, match="at least 8 characters"):
        assert User.parse_obj(invalid)


def test_if_raises_when_password_has_more_than_hundred_characters(valid_data):
    invalid = valid_data | {"password": "a" * 101}
    with pytest.raises(ValidationError, match="has at most 100 characters"):
        assert User.parse_obj(invalid)


def test_if_raises_with_invalid_data(valid_data, invalid_data):
    with pytest.raises(ValidationError):
        User.parse_obj(invalid_data)

    for key in valid_data.keys():
        missing = valid_data.copy()
        with pytest.raises(ValidationError, match=str(key)):
            missing.pop(key)
            User.parse_obj(missing)


def test_if_raises_when_mutating_data(valid_data):
    user = User.parse_obj(valid_data)
    with pytest.raises(TypeError, match='"User" is immutable'):
        user.name = "changed"
