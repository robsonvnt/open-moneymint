from datetime import date
from unittest.mock import Mock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.investment.domain.models import InvestmentModel, AssetType, TransactionModel, TransactionType
from src.investment.repository.db.db_entities import Base, Investment
from src.investment.repository.investment_db_repository import InvestmentRepo
from src.investment.repository.portfolio_db_repository import PortfolioRepo
from src.investment.repository.transaction_db_repository import TransactionRepo
from src.investment.services.investment_service import InvestmentService
from src.investment.services.transaction_service import TransactionService
from tests.investment.prepareto_db_test import add_portfolio, add_investments


@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    testing_session_local = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    db = testing_session_local()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def transaction_service(session):
    portfolio_repo = PortfolioRepo(session)
    investment_repo = InvestmentRepo(session)
    stock_repo = Mock()
    investment_service = InvestmentService(portfolio_repo, investment_repo, stock_repo)

    transaction_repo = TransactionRepo(session)
    transaction_service = TransactionService(transaction_repo, investment_service)
    return transaction_service


def test_calc_avg_purchase_price(transaction_service):
    old_qnt_stocks, old_price, new_qnt_stocks, new_price = 10, 15, 10, 20

    new_price = transaction_service._calc_avg_purchase_price(
        old_qnt_stocks,
        old_price,
        new_qnt_stocks,
        new_price
    )
    assert new_price == 17.5


def create_investment_stock():
    return InvestmentModel(
        code="INV101",
        portfolio_code="POR100",
        asset_type=AssetType.STOCK,
        ticker="STOCK",
        quantity=10,
        purchase_price=15,
        current_average_price=15,
        purchase_date=date.today(),
    )


def create_investment_fixed_income():
    return InvestmentModel(
        code="INV101",
        portfolio_code="POR100",
        asset_type=AssetType.FIXED_INCOME,
        ticker="STOCK",
        quantity=0,
        purchase_price=15,
        current_average_price=18,
        purchase_date=date.today(),
    )


def test_update_investment_buy(transaction_service):
    investment = create_investment_stock()
    transaction = TransactionModel(
        code="TRAN101",
        investment_code="INV100",
        type=TransactionType.BUY,
        date=date.today(),
        quantity=10,
        price=20
    )
    updated_investment = transaction_service._update_investment(investment, transaction)

    assert updated_investment.purchase_price == 17.5
    assert updated_investment.current_average_price == 20
    assert updated_investment.quantity == 20


def test_update_investment_sell(transaction_service):
    investment = create_investment_stock()
    transaction = TransactionModel(
        code="TRAN101",
        investment_code="INV100",
        type=TransactionType.SELL,
        date=date.today(),
        quantity=5,
        price=18.5
    )
    updated_investment = transaction_service._update_investment(investment, transaction)

    assert updated_investment.purchase_price == 15.0
    assert updated_investment.current_average_price == 18.5
    assert updated_investment.quantity == 5


def test_update_investment_interest(transaction_service):
    investment = create_investment_fixed_income()
    transaction = TransactionModel(
        code="TRAN101",
        investment_code="INV100",
        type=TransactionType.INTEREST,
        date=date.today(),
        quantity=0,
        price=3.0
    )
    updated_investment = transaction_service._update_investment(investment, transaction)

    assert updated_investment.purchase_price == 15
    assert updated_investment.current_average_price == 21
    assert updated_investment.quantity == 0


def test_update_investment_deposit(transaction_service):
    investment = create_investment_fixed_income()
    transaction = TransactionModel(
        code="TRAN101",
        investment_code="INV100",
        type=TransactionType.DEPOSIT,
        date=date.today(),
        quantity=0,
        price=3.0
    )
    updated_investment = transaction_service._update_investment(investment, transaction)

    assert updated_investment.purchase_price == 18
    assert updated_investment.current_average_price == 21
    assert updated_investment.quantity == 0


def test_update_investment_withdrawal(transaction_service):
    investment = create_investment_fixed_income()
    transaction = TransactionModel(
        code="TRAN101",
        investment_code="INV100",
        type=TransactionType.WITHDRAWAL,
        date=date.today(),
        quantity=0,
        price=3.0
    )
    updated_investment = transaction_service._update_investment(investment, transaction)

    assert updated_investment.purchase_price == 12
    assert updated_investment.current_average_price == 15
    assert updated_investment.quantity == 0


def test_create_transaction(session, transaction_service):
    add_portfolio(session)
    add_investments(session)

    transaction = TransactionModel(
        code="TRAN101",
        investment_code="INV100",
        type=TransactionType.BUY,
        date=date.today(),
        quantity=10,
        price=530
    )

    transaction_service.create("PORT100", "INV100", transaction)
    inv = transaction_service \
        .investment_service \
        .find_investment_by_code("PORT100", "INV100")

    assert inv.quantity == 60
    assert inv.current_average_price == 530
    assert inv.purchase_price == 505


def test_create_no_investment_update_transaction(session, transaction_service):
    transaction_repo = Mock()
    investment_service = Mock()
    transaction = TransactionModel(
        code="TRAN101",
        investment_code="INV100",
        type=TransactionType.BUY,
        date=date.today(),
        quantity=10,
        price=530
    )

    investment_service.find_investment_by_code.side_effect = (
        Exception("find_investment_by_code não deveria ser chamado"))
    transaction_repo.create.return_value = transaction

    transaction_service = TransactionService(transaction_repo, investment_service)
    transaction_service.create("PORT100", "INV100", transaction, False)

    # asserts
    transaction_repo.create.assert_called_once()


def test_delete_transaction(session, transaction_service):
    transaction_repo = Mock()
    investment_service = Mock()
    transaction = TransactionModel(
        code="TRAN101", investment_code="INV100", type=TransactionType.BUY,
        date=date.today(), quantity=10, price=530
    )
    investment = Investment(
        code="INV100", portfolio_code="PORT100", asset_type="STOCK", ticker="AAPL",
        quantity=50, purchase_price=500.00, current_average_price=510.00, purchase_date=date(2023, 1, 1)
    )

    investment_service.find_investment_by_code.return_value = investment
    transaction_repo.delete.return_value = transaction

    transaction_service = TransactionService(transaction_repo, investment_service)
    transaction_service.delete("PORT100", "INV100", transaction)

    investment_service.refresh_investment_details.assert_called_once()
