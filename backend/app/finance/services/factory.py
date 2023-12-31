from finance.repository.account_consolidation_repository import AccountConsolidationRepo
from finance.repository.account_repository import AccountRepo
from finance.repository.category_repository import CategoryRepo
from finance.repository.financial_transaction_repository import FinancialTransactionRepo
from finance.services.account_consolidation_service import AccountConsolidationService
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
        financial_transaction_repo = FinancialTransactionRepo(session)
        return CategoryService(category_repo, financial_transaction_repo)

    @staticmethod
    def create_financial_transaction_service(session=None) -> FinancialTransactionService:
        account_repo = AccountRepo(session)
        account_service = AccountService(account_repo)
        transaction_repo = FinancialTransactionRepo(session)

        cons_repo = AccountConsolidationRepo(session)
        consolidation_service = AccountConsolidationService(
            cons_repo, transaction_repo, account_repo, None
        )

        return FinancialTransactionService(transaction_repo, account_service, consolidation_service)

    @staticmethod
    def create_account_consolidations_service(session=None) -> AccountConsolidationService:
        transaction_repo = FinancialTransactionRepo(session)
        cons_repo = AccountConsolidationRepo(session)
        account_repo = AccountRepo(session)
        category_repo = CategoryRepo(session)
        return AccountConsolidationService(cons_repo, transaction_repo, account_repo, category_repo)
