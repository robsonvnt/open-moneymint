from typing import Tuple
import pytest
from unittest.mock import Mock, call
from datetime import date

from pydantic import BaseModel

from investment.domains import (
    InvestmentModel,
    PortfolioConsolidationModel,
    PortfolioModel, PortfolioOverviewModel, ConsolidatedPortfolioModel
)
from investment.services.consolidated_service import ConsolidatedPortfolioService


# Helper function to create models
def create_portfolio_overview() -> PortfolioOverviewModel:
    today = date.today()
    return PortfolioOverviewModel(
        code='PortfolioOverviewModel',
        name='PortfolioOverviewModel',
        description='PortfolioOverviewModel',
        amount_invested=700.0,
        current_balance=780.0,
        portfolio_yield=11.4,
        portfolio_gross_nominal_yield=80.0
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


# Função mock que retorna o parâmetro passado
def mock_function(param):
    return param


# Parametrized test to cover different scenarios
@pytest.mark.parametrize("portfolio_code, amount_invested, balance", [
    ('PortfolioOverviewModel', 700.0, 780.0),
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
    model = create_portfolio_overview()
    mock_investment_service.get_portfolio_overview.return_value = model
    mock_cpb_repo.create = Mock(side_effect=mock_function)
    # Act
    consolidated_portfolio = consolidate_portfolio_service.consolidate_portfolio('1234567890')
    # Assert
    mock_cpb_repo.create.assert_called_once()
    assert isinstance(consolidated_portfolio, ConsolidatedPortfolioModel), "my_instance não é uma instância de MyClass"
    assert consolidated_portfolio.portfolio_code == portfolio_code
    assert consolidated_portfolio.amount_invested == amount_invested
    assert consolidated_portfolio.balance == balance
    assert consolidated_portfolio.date == date.today()
