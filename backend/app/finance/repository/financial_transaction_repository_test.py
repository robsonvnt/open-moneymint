from datetime import date
from unittest.mock import Mock, create_autospec

import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from finance.domain.financial_transaction_erros import FinancialTransactionNotFound
from finance.domain.models import FinancialTransactionModel, TransactionType
from finance.repository.db.db_entities import FinancialTransaction
from finance.repository.financial_transaction_repository import FinancialTransactionRepo


def generate_financial_transaction_model(code=None):
    return FinancialTransactionModel(
        code=code, account_code="ACC123", description="Test transaction",
        category_code="CAT123", type=TransactionType.TRANSFER,
        date=date.today(), value=100.0
    )


def generate_financial_transaction(code=None):
    return FinancialTransaction(
        id=1, code=code, account_code="ACC123", description="Test transaction",
        category_code="CAT123", type=TransactionType.TRANSFER,
        date=date.today(), value=100.0
    )


def test_create_financial_transaction():
    mock_session = create_autospec(Session)
    repo = FinancialTransactionRepo(mock_session)
    transaction_data = generate_financial_transaction_model()

    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    result = repo.create(transaction_data)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    assert isinstance(result, FinancialTransactionModel)


def test_find_by_code_successful():
    mock_session = create_autospec(Session)
    repo = FinancialTransactionRepo(mock_session)
    transaction_code = "TRANS123"
    mock_session.query().filter().one.return_value = generate_financial_transaction(transaction_code)

    result = repo.find_by_code(transaction_code)

    assert result.code == transaction_code


def test_find_by_code_not_found():
    mock_session = create_autospec(Session)
    repo = FinancialTransactionRepo(mock_session)
    mock_session.query().filter().one.side_effect = NoResultFound

    with pytest.raises(FinancialTransactionNotFound):
        repo.find_by_code("TRANS123")


def test_filter():
    mock_session = create_autospec(Session)
    repo = FinancialTransactionRepo(mock_session)

    return_value_filter = [
        generate_financial_transaction(),
        generate_financial_transaction(),
    ]

    mock_session.query.return_value.filter.return_value.order_by.return_value.all.return_value = return_value_filter

    result = repo.filter(["TR001"])
    assert mock_session.query.return_value.filter.return_value.order_by.return_value.all.call_count == 1
    assert mock_session.query.call_count == 1
    assert mock_session.query.return_value.filter.call_count == 1
    assert len(result) == 2


def test_filter_with_date():
    mock_session = create_autospec(Session)
    repo = FinancialTransactionRepo(mock_session)

    return_value_filter = [
        generate_financial_transaction(),
        generate_financial_transaction(),
    ]

    query_1 = Mock(name="Mock1")
    query_2 = Mock(name="Mock2")

    query_1.filter.return_value = query_2
    mock_session.query.return_value.filter.return_value = query_1

    query_2.filter.return_value.order_by.return_value.all.return_value = return_value_filter

    result = repo.filter(["TR001"], None, date.today(), date.today())

    assert mock_session.query.call_count == 1
    assert mock_session.query.return_value.filter.call_count == 1
    assert query_1.filter.call_count == 1
    assert query_2.filter.call_count == 1
    assert len(result) == 2


def test_filter_empty_result():
    mock_session = create_autospec(Session)
    repo = FinancialTransactionRepo(mock_session)

    mock_session.query().filter().order_by().all.return_value = []

    result = repo.filter(["TR001"])
    mock_session.query().filter().order_by().all.assert_called_once()
    assert len(result) == 0


def test_update_financial_transaction():
    mock_session = create_autospec(Session)
    repo = FinancialTransactionRepo(mock_session)
    transaction_code = "TRANS123"
    updated_data = generate_financial_transaction_model(transaction_code)
    updated_data.description = "Updated transaction"

    mock_transaction = generate_financial_transaction(transaction_code)
    mock_session.query().filter().one.return_value = mock_transaction
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    result = repo.update(transaction_code, updated_data)

    assert mock_transaction.description == "Updated transaction"
    mock_session.commit.assert_called_once()
    assert result.description == "Updated transaction"


def test_delete_financial_transaction():
    mock_session = create_autospec(Session)
    repo = FinancialTransactionRepo(mock_session)
    transaction_code = "TRANS123"
    mock_transaction = generate_financial_transaction(transaction_code)
    mock_session.query().filter().one.return_value = mock_transaction
    mock_session.delete.return_value = None
    mock_session.commit.return_value = None

    repo.delete(transaction_code)

    mock_session.delete.assert_called_once_with(mock_transaction)
    mock_session.commit.assert_called_once()
