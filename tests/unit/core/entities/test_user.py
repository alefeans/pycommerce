import pytest

from pycommerce.core.entities.user import Email, InvalidUser, Password, User


@pytest.fixture
def valid_data():
    return {
        "name": "Test",
        "email": "test@gmail.com",
        "password": "password",
    }


def test_if_generates_unique_id_for_new_users(valid_data):
    assert User(**valid_data).id != User(**valid_data).id


def test_if_raises_when_password_has_less_than_eight_characters():
    with pytest.raises(InvalidUser):
        User("test", Email("test"), Password("small"))


def test_if_raises_when_password_has_has_more_than_hundred_characters():
    big_password = Password("p" * 101)
    with pytest.raises(InvalidUser):
        User("test", Email("test"), big_password)


@pytest.mark.parametrize(
    "invalid_email",
    [
        (""),
        ("invalid"),
        ("@"),
        ("@.com"),
        ("bla.com"),
        ("@bla.com"),
    ],
)
def test_if_raises_when_email_is_invalid(invalid_email):
    with pytest.raises(InvalidUser):
        User("test", Email(invalid_email), Password("password"))
