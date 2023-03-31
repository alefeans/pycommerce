from typing import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from pycommerce.config import get_settings

DBSession = AsyncSession
engine = create_async_engine(get_settings().DB_URL, future=True)
async_session = sessionmaker(engine, class_=DBSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[DBSession, None]:
    async with async_session() as session:
        yield session
