import pytest
from contextlib import asynccontextmanager
from httpx import AsyncClient
from sqlmodel import SQLModel
from pycommerce.config import get_settings
from pycommerce.infra.db import engine
from pycommerce.infra.api.app import create_app


@pytest.fixture
def settings():
    return get_settings()


@pytest.fixture
def app(settings):
    return create_app(settings)


@asynccontextmanager
async def clear_database():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await engine.dispose()


@pytest.fixture()
async def async_test_client(app, settings):
    base_url = f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}"
    async with clear_database():
        yield AsyncClient(app=app, base_url=base_url)
