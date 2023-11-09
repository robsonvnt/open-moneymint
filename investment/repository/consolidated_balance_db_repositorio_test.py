import pytest
from unittest.mock import create_autospec, Mock, patch

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta

from investment.domains import (
    ConsolidatedPortfolioModel,
    ConsolidatedBalancePortfolioError
)
from investment.repository.consolidated_balance_db_repositorio import ConsolidatedBalanceRepo, \
    ConsolidatedBalancePortfolio, to_database


# from .your_module import ConsolidatedBalancePortfolio, ConsolidatedBalanceRepo, to_database


# Fixture to mock the Session class
@pytest.fixture
def mock_session_factory():
    mock_session = Mock()
    mock_session.__enter__ = Mock(return_value=Mock())
    mock_session.__exit__ = Mock(return_value=True)

    session_factory = Mock(return_value=mock_session)
    return session_factory


# Fixture for the repository with a mocked session
@pytest.fixture
def repo(mock_session_factory):
    return ConsolidatedBalanceRepo(mock_session_factory)


# Test successful date range filtering
def test_filter_by_date_range_success(repo, mock_session_factory):
    start_date = date.today() - timedelta(days=30)
    end_date = date.today()

    # Mock the query chain to return a list of ConsolidatedBalancePortfolio objects
    mock_query_all = mock_session_factory.return_value.query.return_value.filter.return_value.filter.return_value.filter.return_value.order_by.return_value.all
    mock_query_all.return_value = [
        ConsolidatedBalancePortfolio(portfolio_code='001', date=start_date, balance=1000.0, amount_invested=800.0),
        ConsolidatedBalancePortfolio(portfolio_code='001', date=end_date, balance=1100.0, amount_invested=900.0),
    ]

    results = repo.filter_by_date_range(portfolio_code='001', start_date=start_date, end_date=end_date)

    # Verify that results are instances of the domain model
    mock_session_factory.return_value.close.assert_called_once()
    assert all(isinstance(result, ConsolidatedPortfolioModel) for result in results)
    assert len(results) == 2


# Test no records found
def test_filter_by_date_range_no_records(repo, mock_session_factory):
    mock_session_factory.return_value.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
    results = repo.filter_by_date_range(portfolio_code='001')

    mock_session_factory.return_value.close.assert_called_once()
    assert results == []


# Test SQLAlchemyError handling
def test_filter_by_date_range_sqlalchemy_error(repo, mock_session_factory):
    mock_session_factory.return_value.query.side_effect = SQLAlchemyError("Erro Mock")
    result = repo.filter_by_date_range(portfolio_code='001', start_date=date.today(), end_date=date.today())

    mock_session_factory.return_value.close.assert_called_once()
    assert result == ConsolidatedBalancePortfolioError.DatabaseError


# Test unexpected exception handling
def test_filter_by_date_range_unexpected_error(repo, mock_session_factory):
    mock_session_factory.return_value.query.side_effect = Exception("Erro Mock")

    result = repo.filter_by_date_range(portfolio_code='001', start_date=date.today(), end_date=date.today())
    mock_session_factory.return_value.close.assert_called_once()
    assert result == ConsolidatedBalancePortfolioError.Unexpected


# Create method tests
# Test for the 'create' method success scenario
def test_create_success(repo, mock_session_factory):

    # Arrange
    test_model = ConsolidatedPortfolioModel(
        portfolio_code='001',
        date=date.today(),
        balance=1000.0,
        amount_invested=1000.0
    )
    # Act
    result = repo.create(test_model)
    # Assert
    assert isinstance(result, ConsolidatedPortfolioModel)
    mock_session_factory.return_value.add.assert_called_once()
    mock_session_factory.return_value.commit.assert_called_once()
    mock_session_factory.return_value.refresh.assert_called_once()
    mock_session_factory.return_value.close.assert_called_once()


# Test for the 'create' method when a SQLAlchemyError occurs
def test_create_database_error(repo, mock_session_factory):
    # Arrange
    test_model = ConsolidatedPortfolioModel(
        portfolio_code='001',
        date=date.today(),
        balance=1000.0,
        amount_invested=1000.0
    )
    mock_session_factory.return_value.add.side_effect = SQLAlchemyError("Erro Teste")
    result = repo.create(test_model)

    # Assert
    assert result == ConsolidatedBalancePortfolioError.DatabaseError
    mock_session_factory.return_value.close.assert_called_once()

# Test for the 'create' method when an unexpected Exception occurs
def test_create_unexpected_error(repo, mock_session_factory):
    # Arrange
    test_model = ConsolidatedPortfolioModel(
        portfolio_code='001',
        date=date.today(),
        balance=1000.0,
        amount_invested=1000.0
    )
    mock_session_factory.return_value.add.side_effect = Exception("Unexpected Error")
    result = repo.create(test_model)

    # Assert
    assert result == ConsolidatedBalancePortfolioError.Unexpected
    mock_session_factory.return_value.close.assert_called_once()