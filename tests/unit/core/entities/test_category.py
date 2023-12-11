import pytest

from pycommerce.core.entities.category import Category, InvalidCategory


@pytest.fixture
def valid_data():
    return {"name": "Eletronics", "description": "Eletronic devices and artifacts"}


def test_if_generates_unique_id_for_new_categories(valid_data):
    assert Category(**valid_data).id != Category(**valid_data).id


def test_if_raises_when_category_name_is_empty():
    with pytest.raises(InvalidCategory):
        Category("", "Test")


def test_if_raises_when_category_name_has_more_than_hundred_characters():
    with pytest.raises(InvalidCategory):
        Category("t" * 101, "Test")
