import pytest
from unittest.mock import AsyncMock


@pytest.fixture
def async_mocker():
    return lambda name, spec: AsyncMock(name=name, spec=spec)
