import pytest
from unittest.mock import Mock

from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from datetime import date, timedelta

from src.investment.domains import (
    ConsolidatedPortfolioModel,
    ConsolidatedPortfolioError
)
from src.investment.repository.consolidated_balance_db_repository import ConsolidatedBalanceRepo, \
    ConsolidatedPortfolio, to_database


# from .your_module import ConsolidatedBalancePortfolio, ConsolidatedBalanceRepo, to_database

@pytest.fixture
def mock_session():
    return Mock()

# Fixture for the repository with a mocked session
@pytest.fixture
def repo(mock_session):
    return ConsolidatedBalanceRepo(mock_session)


# Test successful date range filtering
def test_filter_by_date_range_success(repo, mock_session):
    start_date = date.today() - timedelta(days=30)
    end_date = date.today()

    # Mock the query chain to return a list of ConsolidatedBalancePortfolio objects
    mock_query_all = mock_session.query.return_value.filter.return_value.filter.return_value.filter.return_value.order_by.return_value.all
    mock_query_all.return_value = [
        ConsolidatedPortfolio(portfolio_code='001', date=start_date, balance=1000.0, amount_invested=800.0),
        ConsolidatedPortfolio(portfolio_code='001', date=end_date, balance=1100.0, amount_invested=900.0),
    ]

    results = repo.filter_by_date_range(portfolio_code='001', start_date=start_date, end_date=end_date)

    # Verify that results are instances of the domain model
    mock_session.close.assert_called_once()
    assert all(isinstance(result, ConsolidatedPortfolioModel) for result in results)
    assert len(results) == 2


# Test no records found
def test_filter_by_date_range_no_records(repo, mock_session):
    mock_session.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
    results = repo.filter_by_date_range(portfolio_code='001')

    mock_session.close.assert_called_once()
    assert results == []


# Test SQLAlchemyError handling
def test_filter_by_date_range_sqlalchemy_error(repo, mock_session):
    mock_session.query.side_effect = SQLAlchemyError("Erro Mock")
    result = repo.filter_by_date_range(portfolio_code='001', start_date=date.today(), end_date=date.today())

    mock_session.close.assert_called_once()
    assert result == ConsolidatedPortfolioError.DatabaseError


# Test unexpected exception handling
def test_filter_by_date_range_unexpected_error(repo, mock_session):
    mock_session.query.side_effect = Exception("Erro Mock")

    result = repo.filter_by_date_range(portfolio_code='001', start_date=date.today(), end_date=date.today())
    mock_session.close.assert_called_once()
    assert result == ConsolidatedPortfolioError.Unexpected


# Create method tests
# Test for the 'create' method success scenario
def test_create_success(repo, mock_session):
    # Arrange
    test_model = ConsolidatedPortfolioModel(
        portfolio_code='001',
        date=date.today(),
        balance=1000.0,
        amount_invested=1000.0
    )
    repo.__get_consolidated_portfolio = Mock()

    mock_session.query.return_value.filter.return_value.filter.return_value.one.side_effect = NoResultFound()

    # Act
    result = repo.create_or_update(test_model)
    # Assert
    assert isinstance(result, ConsolidatedPortfolioModel)
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    assert mock_session.close.call_count == 1


# Update method tests
def test_update_success(repo, mock_session):
    # Arrange
    test_model = ConsolidatedPortfolioModel(
        portfolio_code='001',
        date=date.today(),
        balance=1000.0,
        amount_invested=1000.0
    )
    repo.__get_consolidated_portfolio = Mock()

    mock_session.query.return_value.filter.return_value.filter.return_value.one.return_value = to_database(
        test_model)

    # Act
    result = repo.create_or_update(test_model)
    # Assert
    assert isinstance(result, ConsolidatedPortfolioModel)
    assert mock_session.add.call_count == 0
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    assert mock_session.close.call_count == 1


# Test for the 'create' method when a SQLAlchemyError occurs
def test_create_or_update_database_error(repo, mock_session):
    # Arrange
    test_model = ConsolidatedPortfolioModel(
        portfolio_code='001',
        date=date.today(),
        balance=1000.0,
        amount_invested=1000.0
    )

    mock_session.query.return_value.filter.return_value.filter.return_value.one.return_value = to_database(
        test_model)
    mock_session.refresh.side_effect = SQLAlchemyError("Erro Teste")
    result = repo.create_or_update(test_model)

    # Assert
    assert result == ConsolidatedPortfolioError.DatabaseError
    assert mock_session.close.call_count == 1


# Test for the 'create' method when an unexpected Exception occurs
def test_create_or_update_unexpected_error(repo, mock_session):
    # Arrange
    test_model = ConsolidatedPortfolioModel(
        portfolio_code='001',
        date=date.today(),
        balance=1000.0,
        amount_invested=1000.0
    )
    mock_session.add.side_effect = Exception("Unexpected Error")
    result = repo.create_or_update(test_model)

    # Assert
    assert result == ConsolidatedPortfolioError.Unexpected
