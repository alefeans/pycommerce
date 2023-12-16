from uuid import uuid4

import pytest

from pycommerce.core.dtos.user import CreateUser, UpdateUser
from pycommerce.core.entities.user import Email, InvalidUser, Password
from pycommerce.core.protocols.crypto import Hasher
from pycommerce.core.protocols.user import UserRepo
from pycommerce.core.usecases import user
from tests.unit.core.usecases.fakes.user import FakeUserRepo, FakeUserUnitOfWork, SpyUserHasher


@pytest.fixture
def create_user_dto():
    return CreateUser("Test", Email("test@test.com"), Password("password"))


@pytest.fixture
def user_repo() -> UserRepo:
    return FakeUserRepo()


@pytest.fixture
def hasher() -> Hasher:
    return SpyUserHasher()


@pytest.fixture
def user_uow(user_repo: UserRepo) -> FakeUserUnitOfWork:
    return FakeUserUnitOfWork(user_repo)


async def test_if_creates_user(user_uow, hasher, create_user_dto):
    result = await user.create(user_uow, hasher, create_user_dto)
    persisted_user = await user_uow.user_repo.get_by_id(result.id)

    assert user_uow.committed
    assert create_user_dto.name == persisted_user.name
    assert create_user_dto.email == persisted_user.email
    assert create_user_dto.password != persisted_user.password
    assert hasher.calls == [("hash", create_user_dto.password)]


async def test_if_validates_password_before_hashing(user_uow, hasher):
    user_small_password = CreateUser("Test", Email("test@test.com"), Password("small"))
    with pytest.raises(InvalidUser):
        await user.create(user_uow, hasher, user_small_password)

    user_big_password = CreateUser("Test", Email("test@test.com"), Password("p" * 101))
    with pytest.raises(InvalidUser):
        await user.create(user_uow, hasher, user_big_password)

    assert hasher.calls == []
    assert not user_uow.committed


async def test_if_raises_when_creating_duplicated_user(user_uow, hasher, create_user_dto):
    with pytest.raises(
        user.UserAlreadyExists, match=f"User {create_user_dto.email} already exists"
    ):
        await user.create(user_uow, hasher, create_user_dto)
        await user.create(user_uow, hasher, create_user_dto)
        assert len(user_uow.user_repo) == 1


async def test_if_get_user_by_id(user_uow, hasher, create_user_dto):
    created_user = await user.create(user_uow, hasher, create_user_dto)
    fetched_user = await user.get_by_id(user_uow.user_repo, created_user.id)

    assert fetched_user is not None
    assert created_user.id == fetched_user.id
    assert created_user.name == fetched_user.name
    assert created_user.email == fetched_user.email


async def test_if_returns_none_when_getting_nonexisting_user(user_repo):
    assert await user.get_by_id(user_repo, uuid4()) is None


async def test_if_returns_false_when_deleting_nonexisting_user(user_uow):
    assert await user.delete(user_uow, uuid4()) is False


async def test_if_returns_true_when_deleting_existing_user(user_uow, hasher, create_user_dto):
    created_user = await user.create(user_uow, hasher, create_user_dto)

    assert len(user_uow.user_repo) == 1
    assert await user.delete(user_uow, created_user.id) is True
    assert len(user_uow.user_repo) == 0


async def test_if_updates_user_name(user_uow, hasher, create_user_dto):
    created_user = await user.create(user_uow, hasher, create_user_dto)
    to_update = UpdateUser("changed")

    updated = await user.update(user_uow, created_user.id, to_update)

    assert updated is not None
    assert user_uow.committed
    assert to_update.name == updated.name
    assert created_user.id == updated.id
    assert created_user.name != updated.name
    assert created_user.email == updated.email


async def test_if_updates_user_email(user_uow, hasher, create_user_dto):
    created_user = await user.create(user_uow, hasher, create_user_dto)

    to_update = UpdateUser(email=Email("changed@mail.com"))
    updated = await user.update(user_uow, created_user.id, to_update)

    assert updated is not None
    assert user_uow.committed
    assert to_update.email == updated.email
    assert created_user.id == updated.id
    assert created_user.email != updated.email
    assert created_user.name == updated.name


async def test_if_fully_updates_user(user_uow, hasher, create_user_dto):
    created_user = await user.create(user_uow, hasher, create_user_dto)

    to_update = UpdateUser("changed", email=Email("changed@mail.com"))
    updated = await user.update(user_uow, created_user.id, to_update)

    assert updated is not None
    assert user_uow.committed
    assert to_update.name == updated.name
    assert to_update.email == updated.email
    assert created_user.id == updated.id
    assert created_user.email != updated.email
    assert created_user.name != updated.name


async def test_if_keeps_password_unchanged_when_updating(user_uow, hasher, create_user_dto):
    created_user = await user.create(user_uow, hasher, create_user_dto)
    before_update = await user_uow.user_repo.get_by_id(created_user.id)

    await user.update(user_uow, created_user.id, UpdateUser("changed"))
    after_update = await user_uow.user_repo.get_by_id(created_user.id)

    assert before_update.password == after_update.password


async def test_if_returns_none_when_updating_nonexisting_user(user_uow):
    to_update = UpdateUser("changed", email=Email("changed@mail.com"))
    assert await user.update(user_uow, uuid4(), to_update) is None


async def test_if_authenticates_user(user_uow, hasher, create_user_dto):
    created_user = await user.create(user_uow, hasher, create_user_dto)
    from_repo = await user_uow.user_repo.get_by_id(created_user.id)

    result = await user.authenticate(
        user_uow.user_repo, hasher, create_user_dto.email, create_user_dto.password
    )

    assert result is not None
    assert hasher.calls[-1] == ("verify", f"{create_user_dto.password}, {from_repo.password}")


async def test_if_returns_none_when_authenticating_nonexisting_user(
    user_repo, hasher, create_user_dto
):
    result = await user.authenticate(
        user_repo, hasher, create_user_dto.email, create_user_dto.password
    )

    assert result is None
    assert hasher.calls == []


async def test_if_returns_none_when_authenticating_with_invalid_password(
    user_uow, hasher, create_user_dto
):
    created_user = await user.create(user_uow, hasher, create_user_dto)
    from_repo = await user_uow.user_repo.get_by_id(created_user.id)
    hasher.valid = False
    invalid_password = Password("invalid")

    result = await user.authenticate(
        user_uow.user_repo, hasher, create_user_dto.email, invalid_password
    )

    assert result is None
    assert hasher.calls[-1] == ("verify", f"{invalid_password}, {from_repo.password}")
