from finance.repository.account_repository import AccountRepo
from finance.repository.category_repository import CategoryRepo
from finance.services.account_service import AccountService
from finance.services.category_service import CategoryService


class ServiceFactory:
    @staticmethod
    def create_account_service(session=None) -> AccountService:
        account_repo = AccountRepo(session)
        return AccountService(account_repo)

    @staticmethod
    def create_category_service(session=None) -> CategoryService:
        category_repo = CategoryRepo(session)
        return CategoryService(category_repo)
