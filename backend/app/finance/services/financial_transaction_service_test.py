from datetime import date
from unittest.mock import create_autospec, Mock

import pytest
from unittest.mock import MagicMock, mock_open, patch
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


# Sample data to be used in the tests
csv_content = """01/01/2022;Groceries;-50.00
02/01/2022;Salary;1500.00
"""


# Test for CSV file parsing and transaction creation
def test_create_transactions_from_csv():
    account_code = 'acc321'
    user_code = 'user456'

    # Set up the mocks for dependencies
    mock_repo = MagicMock()
    mock_repo.create = MagicMock()  # Mock the create method to verify calls later
    mock_account_service = MagicMock()
    mock_consolidation_service = MagicMock()

    csv_content = "01/01/2022;Groceries;-50,00\n02/01/2022;Salary;1500,00\n02/01/2022;Salary;1500,00"
    service = FinancialTransactionService(mock_repo, mock_account_service, mock_consolidation_service)

    # Execute the method under test
    service.create_transactions_from_csv(csv_content, account_code, user_code)

    assert mock_repo.create.call_count == 3
    assert mock_account_service.refresh_balance.call_count == 1
    assert mock_consolidation_service.refresh_month_balance.call_count == 2
