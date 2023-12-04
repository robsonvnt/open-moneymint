from datetime import date
from unittest.mock import Mock

import pytest

from finance.domain.models import AccountConsolidationModel, TransactionType, AccountModel, CategoryModel
from finance.repository.category_repository import CategoryRepo
from finance.repository.db.db_entities import FinancialTransaction
from finance.repository.db.prepare_to_db_test import *
from finance.services.account_consolidation_service import AccountConsolidationService


def test_refresh_month_balance():
    account_consolidation_repo = Mock()
    transaction_repo = Mock()
    consolidation_repo = AccountConsolidationService(
        account_consolidation_repo, transaction_repo,
        Mock(), Mock())
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
    account_consolidation_repo.find_by_account_month.return_value = [AccountConsolidationModel(
        account_code="ACC001",
        month=date(2023, 8, 1), balance=100
    )]

    # Tests
    result: AccountConsolidationModel = consolidation_repo.refresh_month_balance("ACC001", date(2023, 12, 1))

    transaction_repo.filter.assert_called_once()
    account_consolidation_repo.find_by_account_month.assert_called_once()
    assert result.balance == 190


def test_get_root_category(memory_db_session):
    add_categories(memory_db_session)

    category_repo = CategoryRepo(memory_db_session)
    service = AccountConsolidationService(Mock(), Mock(), Mock(), category_repo)

    cat = service.get_root_category("CAT009")
    assert cat.code == "CAT001"


# test_get_sum_consolidations_grouped_by_category
@pytest.fixture
def service_with_mocks():
    account_repo = Mock()
    transaction_repo = Mock()
    service = AccountConsolidationService(Mock(), transaction_repo, account_repo, Mock())
    service.get_root_category = Mock()
    return service


# Fixture for the transactions
@pytest.fixture
def transactions():
    return [
        Mock(category_code='cat001', value=100),
        Mock(category_code='cat002', value=200),
        Mock(category_code='cat003', value=50),
        Mock(category_code='cat001', value=300),
    ]


def _get_root_category_mock(code):
    name = "Category 1" if code == "cat001" else "Category 2"
    return CategoryModel(code="1", name=name, parent_category_code=None, user_code="U", created_at=date.today())


def test_get_sum_consolidations_grouped_by_category(service_with_mocks, transactions):
    service_with_mocks.transaction_repo.filter.return_value = transactions
    service_with_mocks.get_root_category.side_effect = _get_root_category_mock

    result = service_with_mocks.get_sum_consolidations_grouped_by_category(
        user_code='user123',
        account_codes=['acc001', 'acc002'],
        date_start=date(2021, 1, 1),
        date_end=date(2021, 12, 31)
    )

    expected_result = [
        {"category": "Category 1", "value": 400},  # 100 + 300 from cat001
        {"category": "Category 2", "value": 250},  # 200 from cat002
    ]
    assert result == expected_result
    assert service_with_mocks.account_repo.find_by_code.call_count == 2
    service_with_mocks.transaction_repo.filter.assert_called_once_with(
        ['acc001', 'acc002'], [], date(2021, 1, 1), date(2021, 12, 31)
    )
    assert service_with_mocks.get_root_category.call_count == len(transactions)
