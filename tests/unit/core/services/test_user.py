import pytest
from pydantic import EmailStr
from pycommerce.core.services import user
from pycommerce.core.services.exceptions import UserAlreadyExists
from pycommerce.core.entities.user import User, CreateUserDTO, UpdateUserDTO
from pycommerce.core.protocols.user import UserRepo
from pycommerce.core.protocols.common import HashingProvider


@pytest.fixture
def create_user_dto():
    return CreateUserDTO(name="Test", email=EmailStr("test@test.com"), password="password")


@pytest.fixture
def update_user_dto():
    return UpdateUserDTO(name="Updated", email=EmailStr("updated@test.com"))


@pytest.fixture
def user_ok(create_user_dto):
    return User.parse_obj(create_user_dto)


@pytest.fixture
def user_repo(async_mocker):
    return async_mocker(name="user_repo", spec=UserRepo)


@pytest.fixture
def hasher(async_mocker):
    return async_mocker(name="hasher", spec=HashingProvider)


async def test_if_creates_user_successfully(user_repo, hasher, create_user_dto, user_ok):
    user_repo.fetch_by_email.return_value = None
    user_repo.persist.return_value = user_ok
    hasher.hash.return_value = "hashed_password"

    result = await user.create(user_repo, hasher, create_user_dto)

    user_repo.persist.assert_called_once()
    user_repo.fetch_by_email.assert_called_once()
    hasher.hash.assert_called_once()
    assert create_user_dto.email == result.email


async def test_if_raises_when_creating_duplicated_user(
    user_repo, hasher, create_user_dto, user_ok
):
    user_repo.fetch_by_email.return_value = user_ok

    with pytest.raises(UserAlreadyExists, match=f"User {user_ok.email} already exists"):
        await user.create(user_repo, hasher, create_user_dto)
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


async def test_if_returns_none_when_updating_nonexisting_user(
    user_repo, user_ok, update_user_dto
):
    user_repo.update.return_value = None
    result = await user.update(user_repo, user_ok.id, update_user_dto)
    user_repo.update.assert_called_once()
    assert result is None


async def test_if_replaces_user_successfully(user_repo, user_ok, update_user_dto):
    user_repo.update.return_value = User(password=user_ok.password, **update_user_dto.dict())
    result = await user.update(user_repo, user_ok.id, update_user_dto)
    user_repo.update.assert_called_once()
    assert result.name == update_user_dto.name  # type: ignore
    assert result.email == update_user_dto.email  # type: ignore


async def test_if_authenticates_user_successfully(user_repo, hasher, user_ok):
    user_repo.fetch_by_email.return_value = user_ok
    hasher.verify.return_value = True

    result = await user.authenticate(user_repo, hasher, user_ok.email, user_ok.password)

    user_repo.fetch_by_email.assert_called_once()
    hasher.verify.assert_called_once()
    assert user_ok.email == result.email  # type: ignore


async def test_if_returns_none_when_authenticating_nonexisting_user(
    user_repo, hasher, user_ok
):
    user_repo.fetch_by_email.return_value = None

    result = await user.authenticate(user_repo, hasher, user_ok.email, user_ok.password)

    user_repo.fetch_by_email.assert_called_once()
    hasher.verify.assert_not_called()
    assert result is None


async def test_if_returns_none_when_authenticating_with_invalid_password(user_repo, hasher, user_ok):
    user_repo.fetch_by_email.return_value = user_ok
    hasher.verify.return_value = False

    result = await user.authenticate(user_repo, hasher, user_ok.email, user_ok.password)

    user_repo.fetch_by_email.assert_called_once()
    hasher.verify.assert_called_once()
    assert result is None
