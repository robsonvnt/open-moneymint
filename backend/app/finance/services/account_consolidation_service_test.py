from datetime import date
from unittest.mock import Mock

from finance.domain.models import AccountConsolidationModel, TransactionType
from finance.repository.db.db_entities import FinancialTransaction
from finance.services.account_consolidation_service import AccountConsolidationService


def test_refresh_month_balance():
    account_consolidation_repo = Mock()
    transaction_repo = Mock()
    consolidation_repo = AccountConsolidationService(account_consolidation_repo, transaction_repo)
    transactions = [
        FinancialTransaction(
            code="TRA001", account_code="ACC123", description="Description 1", category_code="CAT001",
            type=TransactionType.TRANSFER.value, date=date(2023, 5, 5), value=100.0
        ),
        FinancialTransaction(
            code="TRA002", account_code="ACC123", description="Description 2", category_code="CAT003",
            type=TransactionType.DEPOSIT.value, date=date(2023, 5, 10), value=110
        ),
        FinancialTransaction(
            code="TRA003", account_code="ACC123", description="Description 3", category_code="CAT003",
            type=TransactionType.TRANSFER.value, date=date(2023, 6, 5), value=-20
        )]
    transaction_repo.filter.return_value = transactions

    def mock_func(param):
        return param

    account_consolidation_repo.update = mock_func
    account_consolidation_repo.find_by_account_month.return_value = AccountConsolidationModel(
        account_code="ACC001",
        month=date(2023, 8, 1), balance=100
    )

    # Tests
    result: AccountConsolidationModel = consolidation_repo.refresh_month_balance("ACC001", date(2023, 12, 1))

    transaction_repo.filter.assert_called_once()
    account_consolidation_repo.find_by_account_month.assert_called_once()
    assert result.balance == 190
