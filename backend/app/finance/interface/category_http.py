from datetime import date

from fastapi import HTTPException, status, APIRouter
from pydantic import BaseModel
from typing import List, Optional
from fastapi import Depends

from auth.user import User, get_current_user
from finance.domain.category_erros import CategoryNotFound
from finance.domain.models import CategoryModel
from finance.repository.db.db_connection import get_db_session
from finance.services.factory import ServiceFactory

category_router = APIRouter()


class CategoryInput(BaseModel):
    name: str
    parent_category_code: Optional[str]


class CategoryResponse(BaseModel):
    code: str
    name: str
    parent_category_code: Optional[str]
    created_at: date


class CategoryTree(BaseModel):
    code: str
    name: str
    children: List["CategoryTree"]

    @classmethod
    def from_list(cls, categories, parent_code=None):
        tree = []
        for category in categories:
            if category.parent_category_code == parent_code:
                children = cls.from_list(
                    categories, parent_code=category.code
                )
                tree.append(cls(code=category.code, name=category.name, children=children))
        return tree


CategoryTree.model_rebuild()


@category_router.get("/categories", response_model=List[CategoryTree])
async def get_all_categories(
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    category_service = ServiceFactory.create_category_service(db_session)
    categories = category_service.find_all_by_user(current_user.code)
    tree = CategoryTree.from_list(categories)
    return tree


@category_router.get("/categories/{category_code}", response_model=CategoryResponse)
async def get_category(
        category_code: str,
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    try:
        category_service = ServiceFactory.create_category_service(db_session)
        category = category_service.get_by_code(category_code)
        if category.user_code != current_user.code:
            raise CategoryNotFound()
        category_response = CategoryResponse(**category.model_dump())
        return category_response
    except CategoryNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@category_router.post("/categories", response_model=CategoryResponse)
async def create_category(
        input: CategoryInput,
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    category_service = ServiceFactory.create_category_service(db_session)
    category_model = CategoryModel(
        user_code=current_user.code,
        **input.model_dump()
    )
    return category_service.create(category_model)


@category_router.put("/categories/{category_code}", response_model=CategoryResponse)
async def update_category(
        category_code: str,
        category_input: CategoryInput,
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    category_service = ServiceFactory.create_category_service(db_session)
    try:
        # checks if the rented user is the owner of the category
        category = category_service.get_by_code(category_code)
        if category.user_code != current_user.code:
            raise CategoryNotFound()

        for key, value in category_input.model_dump().items():
            setattr(category, key, value)

        updated_category = category_service.update(category_code, category)
        return CategoryResponse(**updated_category.model_dump())
    except CategoryNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


#
@category_router.delete("/categories/{category_code}")
async def delete_category(
        category_code: str,
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    try:
        category_service = ServiceFactory.create_category_service(db_session)

        # checks if the rented user is the owner of the category
        category = category_service.get_by_code(category_code)
        if category.user_code != current_user.code:
            raise CategoryNotFound()

        category_service.delete(category_code)
        return {"message": "Account deleted successfully"}
    except CategoryNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
