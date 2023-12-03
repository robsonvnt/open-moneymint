from datetime import date
from unittest.mock import create_autospec, Mock

import pytest

from finance.domain.models import FinancialTransactionModel, TransactionType
from finance.repository.financial_transaction_repository import FinancialTransactionRepo
from finance.services.account_consolidation_service import AccountConsolidationService
from finance.services.account_service import AccountService
from finance.services.financial_transaction_service import FinancialTransactionService


@pytest.fixture
def mock_financial_transaction_repo():
    return create_autospec(FinancialTransactionRepo)


@pytest.fixture
def mock_account_service():
    return create_autospec(AccountService)


@pytest.fixture
def mock_consolidation_service():
    return create_autospec(AccountConsolidationService)


@pytest.fixture
def transaction_service(
        mock_financial_transaction_repo,
        mock_account_service,
        mock_consolidation_service
):
    return FinancialTransactionService(mock_financial_transaction_repo,
                                       mock_account_service,
                                       mock_consolidation_service)


def generate_financial_transaction_model(code=None):
    return FinancialTransactionModel(
        code=code, account_code="ACC123", description="Test transaction",
        category_code="CAT123", type=TransactionType.TRANSFER,
        date=date.today(), value=100.0
    )


def test_create_transaction_success(transaction_service,
                                    mock_financial_transaction_repo,
                                    mock_account_service,
                                    mock_consolidation_service):
    transaction_model = generate_financial_transaction_model()

    transaction_service.create("U001", transaction_model)

    mock_financial_transaction_repo.create.assert_called_once()
    mock_account_service.refresh_balance.assert_called_once()
    mock_consolidation_service.refresh_month_balance.assert_called_once()


def test_update_transaction_success(transaction_service,
                                    mock_financial_transaction_repo,
                                    mock_account_service,
                                    mock_consolidation_service):
    transaction_model = generate_financial_transaction_model()
    transaction_service.get_by_code = Mock(return_value=generate_financial_transaction_model())

    transaction_service.update("U001", "TRANS001", transaction_model)

    mock_financial_transaction_repo.update.assert_called_once()
    mock_account_service.refresh_balance.assert_called_once()
    mock_consolidation_service.refresh_month_balance.assert_called_once()


def test_delete_transaction_success(transaction_service,
                                    mock_financial_transaction_repo,
                                    mock_account_service,
                                    mock_consolidation_service):
    transaction_service.get_by_code = Mock(return_value=generate_financial_transaction_model())
    mock_financial_transaction_repo.find_by_code = Mock(return_value=generate_financial_transaction_model())

    transaction_service.delete("U001", "TRANS001")

    mock_financial_transaction_repo.delete.assert_called_once()
    mock_account_service.refresh_balance.assert_called_once()
    mock_consolidation_service.refresh_month_balance.assert_called_once()
