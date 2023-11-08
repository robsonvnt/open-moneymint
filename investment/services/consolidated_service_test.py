from typing import Tuple
import pytest
from unittest.mock import Mock, call
from datetime import date

from investment.domains import (
    InvestmentModel,
    PortfolioConsolidationModel,
    PortfolioModel
)
from investment.services.consolidated_service import ConsolidatedPortfolioService


# Helper function to create models
def create_portfolio_consolidation_model() -> PortfolioConsolidationModel:
    today = date.today()
    return PortfolioConsolidationModel(
        portfolio_code='001',
        amount_invested=700.0,
        balance=780.0,
        date=today
    )


# Fixtures for mocks
@pytest.fixture
def mock_cpb_repo() -> Mock:
    return Mock()


@pytest.fixture
def mock_investment_service() -> Mock:
    return Mock()


@pytest.fixture
def consolidate_portfolio_service(mock_cpb_repo: Mock, mock_investment_service: Mock) -> ConsolidatedPortfolioService:
    return ConsolidatedPortfolioService(mock_cpb_repo, mock_investment_service)


# Parametrized test to cover different scenarios
@pytest.mark.parametrize("portfolio_code, amount_invested, balance", [
    ('001', 700.0, 780.0),
    # Add more test cases if necessary
])
def test_consolidate_portfolio(
        portfolio_code: str,
        amount_invested: float,
        balance: float,
        consolidate_portfolio_service: ConsolidatedPortfolioService,
        mock_cpb_repo: Mock,
        mock_investment_service: Mock
):
    """
    Test the consolidation of a portfolio.
    """
    # Arrange
    model = create_portfolio_consolidation_model()
    mock_investment_service.get_portfolio_overview.return_value = model
    # Act
    consolidated_portfolio = consolidate_portfolio_service.consolidate_portfolio('1234567890')
    # Assert
    mock_cpb_repo.create.assert_called_once_with(model)
    assert isinstance(consolidated_portfolio, PortfolioConsolidationModel)
    assert consolidated_portfolio.portfolio_code == portfolio_code
    assert consolidated_portfolio.amount_invested == amount_invested
    assert consolidated_portfolio.balance == balance
    assert consolidated_portfolio.date == model.date
