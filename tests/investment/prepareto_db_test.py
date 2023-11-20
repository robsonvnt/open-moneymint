from unittest.mock import Mock, patch
import tempfile
import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

from src.auth.user import User, get_current_user
from src.investment.repository.db.db_connection import get_db_session
from src.investment.repository.db.db_entities import Base, Portfolio, ConsolidatedPortfolio, Transaction
from src.investment.repository.investment_db_repository import Investment
from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def db_session():
    db_file = tempfile.NamedTemporaryFile(suffix='.sqlite', delete=False)
    db_file_path = db_file.name
    db_file.close()

    # engine = create_engine("sqlite:///.db_test.sqlite", connect_args={"check_same_thread": False})
    engine = create_engine(f"sqlite:///{db_file_path}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        os.remove(db_file_path)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session
    def override_get_current_user():
        return User(name="test", user_name="test", code="001")

    mock_get_price = Mock()
    mock_get_price.return_value.get_price.return_value = 99.99

    with patch('src.investment.repository.factory.RepositoryFactory.create_stock_repo', new=mock_get_price):
        from tests.main_test import app
        app.dependency_overrides[get_db_session] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user

        yield TestClient(app)


def add_portfolio(session):
    session.add(Portfolio(code="PORT100", name="Portfolio Name 100", description="", user_code="001"))
    session.add(Portfolio(code="PORT101", name="Portfolio Name 101", description="", user_code="001"))
    session.commit()


def add_consolidated_portfolio(session):
    session.add(ConsolidatedPortfolio(
        portfolio_code="PORT100", date=date(2023, 1, 1),
        balance=30.0, amount_invested=30.0
    ))
    session.add(ConsolidatedPortfolio(
        portfolio_code="PORT100", date=date(2023, 2, 1),
        balance=30.0, amount_invested=30.0
    ))
    session.add(ConsolidatedPortfolio(
        portfolio_code="PORT100", date=date(2023, 3, 1),
        balance=30.0, amount_invested=30.0
    ))
    session.add(ConsolidatedPortfolio(
        portfolio_code="PORT100", date=date(2023, 4, 1),
        balance=30.0, amount_invested=30.0
    ))
    session.commit()


def add_investments(session):
    session.add(Investment(
        code="INV100", portfolio_code="PORT100", asset_type="STOCK", ticker="AAPL", quantity=50,
        purchase_price=500.00, current_average_price=510.00, purchase_date=date(2023, 1, 1))
    )
    session.add(Investment(
        code="INV101", portfolio_code="PORT100", asset_type="STOCK", ticker="MSFT", quantity=30,
        purchase_price=400.00, current_average_price=210.00, purchase_date=date(2023, 2, 1))
    )
    session.add(Investment(
        code="INV102", portfolio_code="PORT100", asset_type="STOCK", ticker="GOOG", quantity=20,
        purchase_price=300.00, current_average_price=320.00, purchase_date=date(2023, 3, 1))
    )
    session.add(Investment(
        code="INV103", portfolio_code="PORT100", asset_type="FIXED_INCOME", ticker="AMZN", quantity=15,
        purchase_price=200.00, current_average_price=405.00, purchase_date=date(2023, 4, 1))
    )
    session.add(Investment(
        code="INV104", portfolio_code="PORT101", asset_type="FIXED_INCOME", ticker="CDB", quantity=15,
        purchase_price=100.00, current_average_price=510.00, purchase_date=date(2023, 5, 1))
    )
    session.add(Investment(
        code="INV104", portfolio_code="PORT101", asset_type="STOCK", ticker="PETR4", quantity=10,
        purchase_price=100.00, current_average_price=525.00, purchase_date=date(2023, 5, 1))
    )
    session.commit()


def add_transactions(session):
    session.add(Transaction(
        code="TRAN101", investment_code="INV100", type="BUY",
        date=date.fromisoformat("2023-05-02"), quantity=10, price=530
    ))

    session.add(Transaction(
        code="TRAN102", investment_code="INV100", type="SELL",
        date=date.fromisoformat("2023-02-02"), quantity=5, price=530
    ))

    session.add(Transaction(
        code="TRAN103", investment_code="INV100", type="BUY",
        date=date.fromisoformat("2023-08-02"), quantity=5, price=530
    ))

    session.commit()
