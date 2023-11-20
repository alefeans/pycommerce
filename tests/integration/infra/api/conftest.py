from contextlib import asynccontextmanager

import pytest
from httpx import AsyncClient
from sqlmodel import SQLModel

from pycommerce.infra.api.app import create_app
from pycommerce.infra.db import engine


@pytest.fixture
def app(settings):
    return create_app(settings)


@pytest.fixture
def base_url(settings):
    return f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}"


@asynccontextmanager
async def clear_database():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await engine.dispose()


@pytest.fixture()
async def client(app, base_url):
    async with clear_database():
        async with AsyncClient(app=app, base_url=base_url) as async_client:
            yield async_client
