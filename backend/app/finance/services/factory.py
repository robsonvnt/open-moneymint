from finance.repository.account_repository import AccountRepo
from finance.repository.category_repository import CategoryRepo
from finance.repository.financial_transaction_repository import FinancialTransactionRepo
from finance.services.account_service import AccountService
from finance.services.category_service import CategoryService
from finance.services.financial_transaction_service import FinancialTransactionService


class ServiceFactory:
    @staticmethod
    def create_account_service(session=None) -> AccountService:
        account_repo = AccountRepo(session)
        return AccountService(account_repo)

    @staticmethod
    def create_category_service(session=None) -> CategoryService:
        category_repo = CategoryRepo(session)
        return CategoryService(category_repo)

    @staticmethod
    def create_financial_transaction_service(session=None) -> FinancialTransactionService:
        financial_transaction_repo = FinancialTransactionRepo(session)
        return FinancialTransactionService(financial_transaction_repo)