import pytest
from unittest.mock import create_autospec, Mock

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta

from investment.domains import (
    ConsolidatedBalancePortfolioModel,
    ConsolidatedBalancePortfolioError
)
from investment.repository.consolidated_balance_db_repositorio import ConsolidatedBalanceRepo, \
    ConsolidatedBalancePortfolio


# from .your_module import ConsolidatedBalancePortfolio, ConsolidatedBalanceRepo, to_database


# Fixture to mock the Session class
@pytest.fixture
def mock_session():
    return create_autospec(sessionmaker())


# Fixture to mock the database engine
@pytest.fixture
def mock_engine(mock_session):
    engine_mock = Mock()
    engine_mock.connect.return_value = Mock()
    return engine_mock


# Fixture for the repository with a mocked session
@pytest.fixture
def repo(mock_engine, mock_session):
    return ConsolidatedBalanceRepo("url_conection")


# Test successful date range filtering
def test_filter_by_date_range_success(repo, mock_session):
    start_date = date.today() - timedelta(days=30)
    end_date = date.today()

    # Mock the query chain to return a list of ConsolidatedBalancePortfolio objects
    mock_query_all = mock_session.query.return_value.filter.return_value.order_by.return_value.all
    mock_query_all.return_value = [
        ConsolidatedBalancePortfolio(portfolio_code='001', date=start_date, balance=1000.0, amount_invested=800.0),
        ConsolidatedBalancePortfolio(portfolio_code='001', date=end_date, balance=1100.0, amount_invested=900.0),
    ]

    results = repo.filter_by_date_range(portfolio_code='001', start_date=start_date, end_date=end_date)

    # Verify that results are instances of the domain model
    assert all(isinstance(result, ConsolidatedBalancePortfolioModel) for result in results)
    assert len(results) == 2


# Test no records found
def test_filter_by_date_range_no_records(repo, mock_session):
    mock_session.query.return_value.filter.return_value.order_by.return_value.all.return_value = []

    results = repo.filter_by_date_range(portfolio_code='001', start_date=date.today(), end_date=date.today())

    assert results == []


# Test SQLAlchemyError handling
def test_filter_by_date_range_sqlalchemy_error(repo, mock_session):
    mock_session.query.return_value.filter.return_value.order_by.return_value.all.side_effect = SQLAlchemyError

    with pytest.raises(ConsolidatedBalancePortfolioError.DatabaseError):
        repo.filter_by_date_range(portfolio_code='001', start_date=date.today(), end_date=date.today())


# Test unexpected exception handling
def test_filter_by_date_range_unexpected_error(repo, mock_session):
    mock_session.query.return_value.filter.return_value.order_by.return_value.all.side_effect = Exception

    with pytest.raises(ConsolidatedBalancePortfolioError.Unexpected):
        repo.filter_by_date_range(portfolio_code='001', start_date=date.today(), end_date=date.today())
