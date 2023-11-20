from datetime import date, timedelta, datetime

import pytest
from unittest.mock import Mock

from src.investment.domain.investment_errors import UnexpectedError
from src.investment.domain.models import (
    InvestmentModel,
    PortfolioModel, TransactionModel, AssetType, TransactionType
)
from src.investment.domain.transaction_errors import TransactionInvalidType, TransactionOperationNotPermitted
from src.investment.services.investment_service import InvestmentService


# Fixture for the portfolio repository mock
@pytest.fixture
def mock_portfolio_repo():
    return Mock()


# Fixture for the investment repository mock
@pytest.fixture
def mock_investment_repo():
    return Mock()


@pytest.fixture
def mock_stock_repot_repo():
    return Mock()


# Fixture for the investment service
@pytest.fixture
def investment_service(mock_portfolio_repo, mock_investment_repo, mock_stock_repot_repo):
    return InvestmentService(mock_portfolio_repo, mock_investment_repo, mock_stock_repot_repo)


@pytest.fixture
def portfolio():
    return PortfolioModel(code='001', name='test', description='test', user_code='001')


@pytest.fixture
def mock_investment_model():
    return InvestmentModel(
        code="INV123", portfolio_code="PORT456", asset_type=AssetType.STOCK,
        ticker="AAPL", quantity=10.0, purchase_price=150.0,
        current_average_price=155.0, purchase_date=date(2023, 1, 1)
    )


# Test for consolidating a portfolio
def test_get_portfolio_overview_success(investment_service, mock_portfolio_repo, mock_investment_repo, portfolio):
    mock_portfolio_repo.find_by_code.return_value = portfolio
    mock_investment_repo.find_all_by_portfolio_code.return_value = [
        InvestmentModel(code='code1', purchase_price=100, quantity=2, current_average_price=110, portfolio_code='001',
                        asset_type='STOCK', ticker='AAPL', purchase_date=date.today()),
        InvestmentModel(code='code2', purchase_price=50, quantity=10, current_average_price=56, portfolio_code='001',
                        asset_type='STOCK', ticker='MSFT', purchase_date=date.today()),
    ]

    result = investment_service.get_portfolio_overview('001', '001')

    assert result.amount_invested == 700.0
    assert result.portfolio_yield == 11.4
    assert result.portfolio_gross_nominal_yield == 80.0

    # Testando sem nenhum investimento cadastrado
    mock_investment_repo.find_all_by_portfolio_code.return_value = []

    result = investment_service.get_portfolio_overview('001', '001')

    assert result.amount_invested == 0
    assert result.portfolio_yield == 0
    assert result.portfolio_gross_nominal_yield == 0.0
    print(result)


def test_get_portfolio_overview_with_0_values_success(investment_service, mock_portfolio_repo, mock_investment_repo):
    mock_portfolio_repo.find_by_code.return_value = PortfolioModel(code='001', name='test', description='test',
                                                                   user_code='001')
    mock_investment_repo.find_all_by_portfolio_code.return_value = [
        InvestmentModel(code='code1', purchase_price=0, quantity=0, current_average_price=0, portfolio_code='001',
                        asset_type='STOCK', ticker='AAPL', purchase_date=date.today()),
        InvestmentModel(code='code2', purchase_price=0, quantity=0, current_average_price=0, portfolio_code='001',
                        asset_type='STOCK', ticker='MSFT', purchase_date=date.today()),
    ]

    result = investment_service.get_portfolio_overview('001', '001')

    assert result.amount_invested == 0
    assert result.portfolio_yield == 0
    assert result.portfolio_gross_nominal_yield == 0


def test_calculate_investment_details(mock_investment_model, investment_service, mock_investment_repo):
    mock_investment_repo.find_by_code.return_value = mock_investment_model
    investment_service.update = Mock(return_value=mock_investment_model)

    transactions = [
        TransactionModel(
            code="code1", investment_code="INV123", type=TransactionType.BUY, date=date.today(),
            quantity=20, price=100),
        TransactionModel(
            code="code2", investment_code="INV123", type=TransactionType.BUY,
            date=date.today(), quantity=5, price=95),
        TransactionModel(
            code="code3", investment_code="INV123", type=TransactionType.SELL,
            date=date.today(), quantity=20, price=90),
        TransactionModel(
            code="code4", investment_code="INV123", type=TransactionType.BUY,
            date=date.today(), quantity=5, price=110),
        TransactionModel(
            code="code5", investment_code="INV123", type=TransactionType.BUY,
            date=date.today(), quantity=10, price=105)
    ]
    # (2000 + 475 + 550 + 1050) / 40 = 101,875
    # (0 + 475 + 550 + 1050) / 20 = 101,875

    investment_result = investment_service.refresh_investment_details('001', "code123", transactions)

    assert investment_result.purchase_price == 101.88
    assert investment_result.quantity == 20


# Teste para transações de compra
def test_refresh_with_buy_transactions(mock_investment_model, investment_service, mock_investment_repo):
    mock_investment_repo.find_by_code.return_value = mock_investment_model
    investment_service.update = Mock(return_value=mock_investment_model)
    transactions = [
        TransactionModel(code="code1", investment_code="inv123", type=TransactionType.BUY, date=date.today(),
                         quantity=10, price=100),
        TransactionModel(code="code1", investment_code="inv123", type=TransactionType.BUY, date=date.today(),
                         quantity=20, price=110)
    ]

    result = investment_service. \
        refresh_investment_details('001', "inv123", transactions)
    assert result.quantity == 30  # 10 + 20
    assert result.purchase_price == 106.67  # Média ponderada dos preços


# Teste para transações de venda
def test_refresh_with_sell_transactions(mock_investment_model, investment_service, mock_investment_repo):
    mock_investment_repo.find_by_code.return_value = mock_investment_model
    investment_service.update = Mock(return_value=mock_investment_model)
    transactions = [
        TransactionModel(code="code1", investment_code="inv123", type=TransactionType.BUY, date=date.today(),
                         quantity=30, price=100),
        TransactionModel(code="code1", investment_code="inv123", type=TransactionType.SELL,
                         date=date.today() + timedelta(days=1), quantity=10, price=110)
    ]

    result = investment_service.refresh_investment_details('001', "inv123", transactions)
    assert result.quantity == 20  # 30 - 10


# Teste para transação com tipo inválido
def test_refresh_with_invalid_transaction_type(mock_investment_model, investment_service, mock_investment_repo):
    mock_investment_repo.find_by_code.return_value = mock_investment_model
    investment_service.update = Mock(return_value=mock_investment_model)
    transactions = [
        TransactionModel(code="code1", investment_code="inv123", type=TransactionType.DEPOSIT,
                         date=date.today(), quantity=10, price=100)
    ]

    with pytest.raises(TransactionInvalidType):
        investment_service.refresh_investment_details('001', "inv123", transactions)


# Teste para quantidade negativa
def test_refresh_with_negative_quantity(mock_investment_model, investment_service, mock_investment_repo):
    mock_investment_repo.find_by_code.return_value = mock_investment_model
    investment_service.update = Mock(return_value=mock_investment_model)
    transactions = [
        TransactionModel(code="code1", investment_code="inv123", type=TransactionType.BUY, date=date.today(),
                         quantity=30, price=100),
        TransactionModel(code="code1", investment_code="inv123", type=TransactionType.SELL,
                         date=date.today() + timedelta(days=1), quantity=40, price=110)
    ]

    with pytest.raises(TransactionOperationNotPermitted):
        investment_service.refresh_investment_details('001', "inv123", transactions)


# Teste para atualização correta de InvestmentModel
def test_correct_update_of_investment_model(mock_investment_model, investment_service, mock_investment_repo):
    mock_investment_repo.find_by_code.return_value = mock_investment_model
    investment_service.update = Mock(return_value=mock_investment_model)
    yesterday = datetime.now() - timedelta(days=1)
    transactions = [
        TransactionModel(code="code1", investment_code="inv123", type=TransactionType.BUY,
                         date=yesterday.date(), quantity=10, price=100),
        TransactionModel(code="code1", investment_code="inv123", type=TransactionType.BUY, date=date.today(),
                         quantity=20, price=110)
    ]

    result = investment_service.refresh_investment_details('001', "inv123", transactions)
    assert result.current_average_price == 110  # Preço da transação mais recente
    assert result.purchase_price == 106.67  # Média ponderada dos preços
