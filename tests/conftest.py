import pytest
from unittest.mock import AsyncMock
from pycommerce.config import get_settings


@pytest.fixture
def async_mocker():
    return lambda name, spec: AsyncMock(name=name, spec=spec)


@pytest.fixture
def settings():
    return get_settings()
