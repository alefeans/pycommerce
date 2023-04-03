import pytest
from pydantic import EmailStr
from pycommerce.core.services import user
from pycommerce.core.services.exceptions import UserAlreadyExists
from pycommerce.core.entities.user import User, CreateUserDTO
from pycommerce.core.protocols.user import UserRepo
from pycommerce.core.protocols.common import HashingProvider


@pytest.fixture
def create_user_dto():
    return CreateUserDTO(name="Test", email=EmailStr("test@gmail.com"), password="password")


@pytest.fixture
def user_ok(create_user_dto):
    return User.parse_obj(create_user_dto)


@pytest.fixture
def user_repo(async_mocker):
    return async_mocker(name="user_repo", spec=UserRepo)


@pytest.fixture
def hashing_provider(async_mocker):
    return async_mocker(name="hashing_provider", spec=HashingProvider)


async def test_if_creates_user_successfully(
    user_repo, hashing_provider, create_user_dto, user_ok
):
    user_repo.fetch_by_email.return_value = None
    user_repo.persist.return_value = user_ok
    hashing_provider.hash.return_value = "hashed_password"

    result = await user.create(user_repo, hashing_provider, create_user_dto)

    user_repo.persist.assert_called_once()
    user_repo.fetch_by_email.assert_called_once()
    hashing_provider.hash.assert_called_once()
    assert create_user_dto.email == result.email


async def test_if_raises_when_creating_duplicated_user(
    user_repo, hashing_provider, create_user_dto, user_ok
):
    user_repo.fetch_by_email.return_value = user_ok

    with pytest.raises(UserAlreadyExists, match=f"User {user_ok.email} already exists"):
        await user.create(user_repo, hashing_provider, create_user_dto)
    user_repo.fetch_by_email.assert_called_once()
    user_repo.persist.assert_not_called()


async def test_if_fetches_user_by_id(user_repo, user_ok):
    user_repo.fetch_by_id.return_value = user_ok
    result = await user.fetch_by_id(user_repo, user_ok.id)
    user_repo.fetch_by_id.assert_called_once()
    assert user_ok.id == result.id  # type: ignore


async def test_if_returns_none_when_fetching_nonexisting_user(user_repo, user_ok):
    user_repo.fetch_by_id.return_value = None
    result = await user.fetch_by_id(user_repo, user_ok.id)
    user_repo.fetch_by_id.assert_called_once()
    assert result is None


async def test_if_returns_false_when_deleting_nonexisting_user(user_repo, user_ok):
    user_repo.delete.return_value = False
    result = await user.delete(user_repo, user_ok.id)
    user_repo.delete.assert_called_once()
    assert result is False


async def test_if_returns_true_when_deleting_existing_user(user_repo, user_ok):
    user_repo.delete.return_value = True
    result = await user.delete(user_repo, user_ok.id)
    user_repo.delete.assert_called_once()
    assert result is True
