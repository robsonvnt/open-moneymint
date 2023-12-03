from datetime import date

from finance.domain.account_erros import AccountConsolidationNotFound
from finance.domain.models import AccountConsolidationModel
from finance.repository.account_consolidation_repository import AccountConsolidationRepo
from finance.repository.financial_transaction_repository import FinancialTransactionRepo
from helpers import get_last_day_of_the_month


class AccountConsolidationService:
    def __init__(
            self,
            account_consolidation_repo: AccountConsolidationRepo,
            transaction_repo: FinancialTransactionRepo
    ):
        self.account_consolidation_repo = account_consolidation_repo
        self.transaction_repo = transaction_repo

    def create(self, new_consolidation_data: AccountConsolidationModel):
        return self.account_consolidation_repo.create(new_consolidation_data)

    def find_by_account_month(self, account_code: str, month: date):
        return self.account_consolidation_repo.find_by_account_month(account_code, month)

    def find_all_by_account(
            self, account_code: str, start_month: date = None, end_month: date = None
    ):
        return self.account_consolidation_repo.find_all_by_account(account_code, start_month, end_month)

    def refresh_month_balance(
            self,
            account_code: str,
            month: date
    ):
        transactions = self.transaction_repo.filter(
            account_codes=[account_code],
            category_codes=None,
            date_start=date(month.year, month.month, 1),
            date_end=get_last_day_of_the_month(month)
        )
        balance = 0.0
        for transaction in transactions:
            balance += transaction.value

        try:
            consolidation = self.account_consolidation_repo.find_by_account_month(account_code, month)
        except AccountConsolidationNotFound:
            new_consolidation = AccountConsolidationModel(
                account_code=account_code,
                month=month,
                balance=balance
            )
            consolidation = self.account_consolidation_repo.create(new_consolidation)

        consolidation.balance = balance
        return self.account_consolidation_repo.update(consolidation)
