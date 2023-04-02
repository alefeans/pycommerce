import pytest
from httpx import AsyncClient
from tests.utils.db import clear_database
from pycommerce.infra.api.app import create_app


@pytest.fixture
def app(settings):
    return create_app(settings)


@pytest.fixture()
async def client(settings, app):
    base_url = f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}"
    async with clear_database():
        async with AsyncClient(app=app, base_url=base_url) as async_client:
            yield async_client
