from datetime import date
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

from finance.domain.models import FinancialTransactionModel, TransactionType
from finance.repository.financial_transaction_repository import FinancialTransactionRepo
from finance.services.account_consolidation_service import AccountConsolidationService
from finance.services.account_service import AccountService


class FinancialTransactionService:
    def __init__(
            self,
            financial_transaction_repo: FinancialTransactionRepo,
            account_service: AccountService,
            consolidation_service: AccountConsolidationService
    ):
        self.financial_transaction_repo = financial_transaction_repo
        self.account_service = account_service
        self.consolidation_service = consolidation_service

    def create(self, user_code: str, new_transaction: FinancialTransactionModel) -> FinancialTransactionModel:
        created_transaction = self.financial_transaction_repo.create(new_transaction)
        self.account_service.refresh_balance(user_code, created_transaction.account_code)
        self.consolidation_service.refresh_month_balance(new_transaction.account_code, new_transaction.date)
        return created_transaction

    def get_by_code(self, transaction_code: str) -> FinancialTransactionModel:
        return self.financial_transaction_repo.find_by_code(transaction_code)

    def filter_by_account_and_date(
            self,
            user_code: str,
            account_codes: List[str],
            category_codes: Optional[List[str]],
            date_start: date = None,
            date_end: date = None
    ) -> List[FinancialTransactionModel]:

        for acc in account_codes:
            self.account_service.get_by_code(user_code, acc)

        return self.financial_transaction_repo.filter(
            account_codes, category_codes, date_start, date_end
        )

    def update(
            self, user_code: str, transaction_code: str, updated_transaction: FinancialTransactionModel
    ) -> FinancialTransactionModel:
        db_transaction_account_code = self.get_by_code(transaction_code).account_code
        tran_result = self.financial_transaction_repo.update(transaction_code, updated_transaction)
        self.account_service.refresh_balance(user_code, tran_result.account_code)
        if db_transaction_account_code != updated_transaction.account_code:
            self.account_service.refresh_balance(user_code, db_transaction_account_code)
        self.consolidation_service.refresh_month_balance(updated_transaction.account_code, updated_transaction.date)
        return tran_result

    def delete(self, user_code: str, transaction_code: str):
        account_code = self.get_by_code(transaction_code).account_code
        transaction = self.financial_transaction_repo.find_by_code(transaction_code)
        self.financial_transaction_repo.delete(transaction_code)
        self.account_service.refresh_balance(user_code, account_code)
        self.consolidation_service.refresh_month_balance(account_code, transaction.date)

    def create_transactions_from_csv(self, file_content: str, account_code: str, user_code: str):
        import csv
        print(f"account_code: {account_code}")
        lines = file_content.split('\n')
        date_to_consolidate = set([])
        for line in lines:
            row = line.split(';')
            transaction_date = datetime.strptime(row[0], "%d/%m/%Y").date()
            date_to_consolidate.add(transaction_date)
            description = row[1]
            value = float(Decimal(row[2].replace(',', '.')))
            transaction_type = TransactionType.WITHDRAWAL if value < 0 else TransactionType.DEPOSIT

            new_transaction = FinancialTransactionModel(
                account_code=account_code,
                description=description,
                category_code=None,
                type=transaction_type,
                date=transaction_date,
                value=value
            )
            self.financial_transaction_repo.create(new_transaction)
        self.account_service.refresh_balance(user_code, account_code)
        for date in list(date_to_consolidate):
            self.consolidation_service.refresh_month_balance(account_code, date)
