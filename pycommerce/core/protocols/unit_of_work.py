from typing import Protocol


class UnitOfWork(Protocol):
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

    async def commit(self):
        ...

    async def rollback(self):
        ...
