from datetime import datetime, date

import pytest
from decimal import Decimal
from unittest.mock import Mock

from investment.domains import (
    InvestmentModel,
    PortfolioConsolidationModel,
    InvestmentError,
    PortfolioError,
    PortfolioModel
)
from investment.services.investment_service import InvestmentService


# Fixture for the portfolio repository mock
@pytest.fixture
def mock_portfolio_repo():
    return Mock()


# Fixture for the investment repository mock
@pytest.fixture
def mock_investment_repo():
    return Mock()


# Fixture for the investment service
@pytest.fixture
def investment_service(mock_portfolio_repo, mock_investment_repo):
    return InvestmentService(mock_portfolio_repo, mock_investment_repo)


# Test for consolidating a portfolio
def test_consolidate_portfolio(investment_service, mock_portfolio_repo, mock_investment_repo):
    mock_portfolio_repo.find_by_code.return_value = PortfolioModel(code='001', name='test', description='test')
    mock_investment_repo.find_all_by_portfolio_code.return_value = [
        InvestmentModel(code='code1', purchase_price=100, quantity=2, current_average_price=110, portfolio_code='001',
                        asset_type='stock', ticker='AAPL', purchase_date=date.today()),
        InvestmentModel(code='code1', purchase_price=50, quantity=10, current_average_price=56, portfolio_code='001',
                        asset_type='stock', ticker='MSFT', purchase_date=date.today()),
    ]

    result = investment_service.consolidate_portfolio('001')
    assert isinstance(result, PortfolioConsolidationModel)
    assert result.amount_invested == 700.0
    assert result.portfolio_yield == 11.4
    assert result.portfolio_gross_nominal_yield == 80.0


# Add more tests as needed for full coverage
