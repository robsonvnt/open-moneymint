from collections import defaultdict
from datetime import date
from typing import List

from finance.domain.account_erros import AccountConsolidationNotFound
from finance.domain.models import AccountConsolidationModel, TransactionType
from finance.repository.account_consolidation_repository import AccountConsolidationRepo
from finance.repository.account_repository import AccountRepo
from finance.repository.category_repository import CategoryRepo
from finance.repository.financial_transaction_repository import FinancialTransactionRepo
from helpers import get_last_day_of_the_month


class AccountConsolidationService:
    def __init__(
            self,
            account_consolidation_repo: AccountConsolidationRepo,
            transaction_repo: FinancialTransactionRepo,
            account_repo: AccountRepo,
            category_repo: CategoryRepo
    ):
        self.account_consolidation_repo = account_consolidation_repo
        self.transaction_repo = transaction_repo
        self.account_repo = account_repo
        self.category_repo = category_repo

    def create(self, new_consolidation_data: AccountConsolidationModel):
        return self.account_consolidation_repo.create(new_consolidation_data)

    def find_by_account_month(self, account_codes: List[str], month: date):
        return self.account_consolidation_repo.find_by_account_month(account_codes, month)

    def find_all_by_account(
            self, account_codes: List[str], start_month: date = None, end_month: date = None
    ):
        return self.account_consolidation_repo.find_all_by_account(account_codes, start_month, end_month)

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

        consolidations = self.account_consolidation_repo.find_by_account_month([account_code], month)
        if len(consolidations) > 0:
            consolidation = consolidations[0]
            consolidation.balance = balance
            return self.account_consolidation_repo.update(consolidation)
        else:
            new_consolidation = AccountConsolidationModel(
                account_code=account_code,
                month=date(month.year, month.month, 1),
                balance=balance
            )
            return self.account_consolidation_repo.create(new_consolidation)

    def get_root_category(self, category_code):
        category = self.category_repo.find_by_code(category_code)
        if category.parent_category_code:
            category = self.get_root_category(category.parent_category_code)
        return category

    def get_sum_consolidations_grouped_by_category(
            self,
            user_code: str,
            account_codes: List[str],
            date_start: date = None,
            date_end: date = None
    ):
        for acc in account_codes:
            self.account_repo.find_by_code(user_code, acc)

        transactions = self.transaction_repo.filter(account_codes, [], date_start, date_end)
        result = defaultdict(float)
        for t in transactions:
            if t.type != TransactionType.DEPOSIT:
                if t.category_code:
                    result[self.get_root_category(t.category_code).name] += t.value
                else:
                    result["Não categorizado"] += t.value

        return [{"category": key, "value": value} for key, value in result.items()]




