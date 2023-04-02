from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from pycommerce.infra.db import engine


@asynccontextmanager
async def clear_database():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await engine.dispose()
