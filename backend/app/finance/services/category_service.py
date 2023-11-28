from typing import List

from finance.domain.category_erros import CategoryNotFound, CategoryUnexpectedError, CategoryOperationNotPermittedError
from finance.domain.models import CategoryModel
from finance.repository.category_repository import CategoryRepo
from finance.repository.financial_transaction_repository import FinancialTransactionRepo


class CategoryService:
    def __init__(self, category_repo: CategoryRepo, transaction_repo: FinancialTransactionRepo):
        self.category_repo = category_repo
        self.transaction_repo = transaction_repo

    def create(self, new_category: CategoryModel) -> CategoryModel:
        return self.category_repo.create(new_category)

    def get_by_code(self, category_code: str) -> CategoryModel:
        return self.category_repo.find_by_code(category_code)

    def update(self, category_code: str, updated_category: CategoryModel) -> CategoryModel:
        if updated_category.code != category_code:
            raise CategoryOperationNotPermittedError("Code cannot be changed.")
        return self.category_repo.update(category_code, updated_category)

    def delete(self, category_code: str):
        transactions = self.transaction_repo.filter(
            None,
            [category_code]
        )
        for transaction in transactions:
            transaction.category_code = None
            self.transaction_repo.update(transaction.code, transaction)
        self.category_repo.delete(category_code)

    def find_categories_by_user_and_parent(
            self, user_code: str, parent_category_code: str = None
    ) -> List[CategoryModel]:
        return self.category_repo.find_categories_by_user_and_parent(user_code, parent_category_code)

    def find_all_by_user(self, user_code: str) -> List[CategoryModel]:
        return self.category_repo.find_all_by_user(user_code)

    def _find_children(self, category_code: str, categories: List[CategoryModel]):
        children = []
        for cat in categories:
            atualcode = cat.parent_category_code
            if cat.parent_category_code == category_code:
                children.append(cat)
                sub_children = self._find_children(cat.code, categories)
                children.extend(sub_children)
        return children

    def list_all_children(self, category_code: str, user_code: str):
        all_user_categories = self.find_all_by_user(user_code)
        return self._find_children(category_code, all_user_categories)
