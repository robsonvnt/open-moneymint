from datetime import date

from finance.domain.models import FinancialTransactionModel
from finance.repository.financial_transaction_repository import FinancialTransactionRepo
from typing import List


class FinancialTransactionService:
    def __init__(self, financial_transaction_repo: FinancialTransactionRepo):
        self.financial_transaction_repo = financial_transaction_repo

    def create(self, new_transaction: FinancialTransactionModel) -> FinancialTransactionModel:
        return self.financial_transaction_repo.create(new_transaction)

    def get_by_code(self, transaction_code: str) -> FinancialTransactionModel:
        return self.financial_transaction_repo.find_by_code(transaction_code)

    def filter_by_account_and_date(
            self, account_codes: List[str],
            date_start: date = None, date_end: date = None
    ) -> List[FinancialTransactionModel]:
        return self.financial_transaction_repo.filter_by_account_and_date(
            account_codes, date_start, date_end
        )

    def update(
            self, transaction_code: str, updated_transaction: FinancialTransactionModel
    ) -> FinancialTransactionModel:
        return self.financial_transaction_repo.update(transaction_code, updated_transaction)

    def delete(self, transaction_code: str):
        self.financial_transaction_repo.delete(transaction_code)
