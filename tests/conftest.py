import pytest

from pycommerce.config import get_settings


@pytest.fixture
def settings():
    return get_settings()
