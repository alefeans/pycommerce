import pytest
from httpx import AsyncClient
from pycommerce.infra.api.app import create_app
from pycommerce.config import get_settings


@pytest.fixture
def settings():
    return get_settings()


@pytest.fixture
def app(settings):
    return create_app(settings)
