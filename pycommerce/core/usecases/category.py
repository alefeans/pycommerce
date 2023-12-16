from typing import List, Optional
from uuid import UUID

from pycommerce.core.dtos.category import CategoryResponse, CreateCategory, UpdateCategory
from pycommerce.core.entities.category import Category
from pycommerce.core.protocols.category import CategoryRepo, CategoryUnitOfWork


class CategoryAlreadyExists(Exception):
    pass


async def create(uow: CategoryUnitOfWork, dto: CreateCategory) -> CategoryResponse:
    async with uow:
        if await uow.category_repo.get_by_name(dto.name):
            raise CategoryAlreadyExists(f"Category {dto.name} already exists")

        category = Category(dto.name, dto.description)
        await uow.category_repo.persist(category)
        return CategoryResponse(
            category.id, category.name, category.description, category.created_date
        )


async def get_all(repo: CategoryRepo) -> List[CategoryResponse]:
    return [
        CategoryResponse(ctg.id, ctg.name, ctg.description, ctg.created_date)
        for ctg in await repo.get_all()
    ]


async def get_by_id(repo: CategoryRepo, _id: UUID) -> Optional[CategoryResponse]:
    category = await repo.get_by_id(_id)
    if category:
        return CategoryResponse(
            category.id, category.name, category.description, category.created_date
        )


async def delete(uow: CategoryUnitOfWork, _id: UUID) -> bool:
    async with uow:
        return await uow.category_repo.delete(_id)


async def update(
    uow: CategoryUnitOfWork, _id: UUID, dto: UpdateCategory
) -> Optional[CategoryResponse]:
    async with uow:
        existing_category = await uow.category_repo.get_by_id(_id)

        if existing_category is None:
            return None

        updated_category = await uow.category_repo.update(
            Category(
                dto.name or existing_category.name,
                dto.description or existing_category.description,
                existing_category.id,
                existing_category.created_date,
            )
        )

        if updated_category:
            return CategoryResponse(
                updated_category.id,
                updated_category.name,
                updated_category.description,
                updated_category.created_date,
            )
