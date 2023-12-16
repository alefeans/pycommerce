from uuid import uuid4

import pytest

from pycommerce.core.dtos.category import CreateCategory, UpdateCategory
from pycommerce.core.protocols.category import CategoryRepo
from pycommerce.core.usecases import category
from tests.unit.core.usecases.fakes.category import FakeCategoryRepo, FakeCategoryUnitOfWork


@pytest.fixture
def create_category_dto():
    return CreateCategory("Test", "Test description")


@pytest.fixture
def category_repo() -> CategoryRepo:
    return FakeCategoryRepo()


@pytest.fixture
def category_uow(category_repo: CategoryRepo) -> FakeCategoryUnitOfWork:
    return FakeCategoryUnitOfWork(category_repo)


async def test_if_creates_category(category_uow, create_category_dto):
    result = await category.create(category_uow, create_category_dto)
    persisted_category = await category_uow.category_repo.get_by_id(result.id)

    assert category_uow.committed
    assert create_category_dto.name == persisted_category.name
    assert create_category_dto.description == persisted_category.description
    assert persisted_category.created_at is not None


async def test_if_raises_when_creating_duplicated_category(category_uow, create_category_dto):
    with pytest.raises(
        category.CategoryAlreadyExists,
        match=f"Category {create_category_dto.name} already exists",
    ):
        await category.create(category_uow, create_category_dto)
        await category.create(category_uow, create_category_dto)

        assert len(category_uow.category_repo) == 1


async def test_if_get_all_categories(category_uow, create_category_dto):
    await category.create(category_uow, create_category_dto)
    await category.create(category_uow, CreateCategory("Other", "Other description"))
    categories = await category.get_all(category_uow.category_repo)

    assert len(categories) == 2


async def test_if_get_all_returns_empty_list_for_empty_store(
    category_uow, create_category_dto
):
    categories = await category.get_all(category_uow.category_repo)

    assert categories == []
    assert len(categories) == 0


async def test_if_get_category_by_id(category_uow, create_category_dto):
    created_category = await category.create(category_uow, create_category_dto)
    fetched_category = await category.get_by_id(
        category_uow.category_repo, created_category.id
    )

    assert fetched_category is not None
    assert created_category.id == fetched_category.id
    assert created_category.name == fetched_category.name
    assert created_category.description == fetched_category.description
    assert created_category.created_at == fetched_category.created_at


async def test_if_returns_none_when_getting_nonexisting_category(category_repo):
    assert await category.get_by_id(category_repo, uuid4()) is None


async def test_if_returns_false_when_deleting_nonexisting_category(category_uow):
    assert await category.delete(category_uow, uuid4()) is False


async def test_if_returns_true_when_deleting_existing_category(
    category_uow, create_category_dto
):
    created_category = await category.create(category_uow, create_category_dto)

    assert len(category_uow.category_repo) == 1
    assert await category.delete(category_uow, created_category.id) is True
    assert len(category_uow.category_repo) == 0


async def test_if_updates_category_name(category_uow, create_category_dto):
    created_category = await category.create(category_uow, create_category_dto)
    to_update = UpdateCategory("Updated")

    updated = await category.update(category_uow, created_category.id, to_update)

    assert updated is not None
    assert category_uow.committed
    assert to_update.name == updated.name
    assert created_category.id == updated.id
    assert created_category.name != updated.name
    assert created_category.created_at == updated.created_at
    assert created_category.description == updated.description


async def test_if_updates_category_description(category_uow, create_category_dto):
    created_category = await category.create(category_uow, create_category_dto)
    to_update = UpdateCategory(description="Updated")

    updated = await category.update(category_uow, created_category.id, to_update)

    assert updated is not None
    assert category_uow.committed
    assert to_update.description == updated.description
    assert created_category.id == updated.id
    assert created_category.name == updated.name
    assert created_category.description != updated.description
    assert created_category.created_at == updated.created_at


async def test_if_fully_updates_category(category_uow, create_category_dto):
    created_category = await category.create(category_uow, create_category_dto)
    to_update = UpdateCategory("Updated", "Updated description")

    updated = await category.update(category_uow, created_category.id, to_update)

    assert updated is not None
    assert category_uow.committed
    assert to_update.name == updated.name
    assert created_category.id == updated.id
    assert to_update.description == updated.description
    assert created_category.name != updated.name
    assert created_category.description != updated.description
    assert created_category.created_at == updated.created_at


async def test_if_returns_none_when_updating_nonexisting_category(category_uow):
    to_update = UpdateCategory("Changed", "New description")
    assert await category.update(category_uow, uuid4(), to_update) is None
