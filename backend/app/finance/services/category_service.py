from typing import List

from finance.domain.category_erros import CategoryNotFound, CategoryUnexpectedError, CategoryOperationNotPermittedError
from finance.domain.models import CategoryModel
from finance.repository.category_repository import CategoryRepo


class CategoryService:
    def __init__(self, category_repo: CategoryRepo):
        self.category_repo = category_repo

    def create(self, new_category: CategoryModel) -> CategoryModel:
        return self.category_repo.create(new_category)

    def get_by_code(self, category_code: str) -> CategoryModel:
        return self.category_repo.find_by_code(category_code)

    def update(self, category_code: str, updated_category: CategoryModel) -> CategoryModel:
        if updated_category.code != category_code:
            raise CategoryOperationNotPermittedError("Code cannot be changed.")
        return self.category_repo.update(category_code, updated_category)

    def delete(self, category_code: str):
        self.category_repo.delete(category_code)

    def find_all(self, user_code: str, parent_category_code: str) -> List[CategoryModel]:
        return self.category_repo.find_all(user_code, parent_category_code)
