from typing import AsyncGenerator
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from pycommerce.config import get_settings

DBSession = AsyncSession
engine = create_async_engine(get_settings().DB_URL)
async_session = sessionmaker(engine, class_=DBSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[DBSession, None]:
    async with async_session() as session:
        yield session
