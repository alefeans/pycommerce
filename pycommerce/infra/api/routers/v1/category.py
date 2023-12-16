from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException

from pycommerce.core.dtos.category import CategoryResponse, CreateCategory, UpdateCategory
from pycommerce.core.entities.category import InvalidCategory
from pycommerce.core.usecases import category
from pycommerce.infra.api.dependencies.category import Repo, UnitOfWork

router = APIRouter()


@router.post(
    "",
    status_code=201,
    summary="Creates new Category",
    responses={
        201: {"description": "Category created successfully"},
        409: {"description": "Category already exists"},
    },
)
async def create(dto: CreateCategory, uow: UnitOfWork) -> CategoryResponse:
    try:
        return await category.create(uow, dto)
    except InvalidCategory as e:
        raise HTTPException(422, detail=f"Invalid category: {e}")
    except category.CategoryAlreadyExists:
        raise HTTPException(409, detail="Category already exists")


@router.get(
    "/{category_id}",
    summary="Gets Category information",
    responses={
        200: {"description": "Category found"},
        404: {"description": "Category not found"},
    },
)
async def get(category_id: UUID, repo: Repo) -> CategoryResponse:
    response = await category.get_by_id(repo, category_id)
    if not response:
        raise HTTPException(status_code=404, detail="Category not found")
    return response


@router.get(
    "",
    summary="Gets all Categories",
    responses={
        200: {"description": "Categories found"},
        404: {"description": "Categories not found"},
    },
)
async def get_all(repo: Repo) -> List[CategoryResponse]:
    response = await category.get_all(repo)
    if not response:
        raise HTTPException(status_code=404, detail="Categories not found")
    return response


@router.delete(
    "/{category_id}",
    status_code=204,
    summary="Deletes Category",
    responses={
        204: {"description": "Category deleted successfully"},
        404: {"description": "Category not found"},
    },
)
async def delete(category_id: UUID, uow: UnitOfWork) -> None:
    if not await category.delete(uow, category_id):
        raise HTTPException(status_code=404, detail="Category not found")


@router.patch(
    "/{category_id}",
    summary="Updates Category information",
    responses={
        200: {"description": "Category updated"},
        404: {"description": "Category not found"},
    },
)
async def patch(category_id: UUID, dto: UpdateCategory, uow: UnitOfWork) -> CategoryResponse:
    response = await category.update(uow, category_id, dto)
    if not response:
        raise HTTPException(status_code=404, detail="Category not found")
    return response
