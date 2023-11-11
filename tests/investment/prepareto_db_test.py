import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

from src.investment.repository.db_connection import get_db_session
from src.investment.repository.db_entities import Base, Portfolio
from src.investment.repository.investment_db_repository import Investment
from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    from src.main import app
    app.dependency_overrides[get_db_session] = override_get_db  # 'get_db' é a função de dependência original
    yield TestClient(app)


def add_portfolio(session):
    session.add(Portfolio(code="PORT100", name="Portfolio Name", description=""))
    session.commit()


def add_investments(session):
    session.add(Investment(code="INV100", portfolio_code="PORT100", asset_type="Stock", ticker="AAPL", quantity=50,
                           purchase_price=500.00, current_average_price=110.00, purchase_date=date(2023, 1, 1)))
    session.add(Investment(code="INV101", portfolio_code="PORT100", asset_type="Bond", ticker="MSFT", quantity=30,
                           purchase_price=400.00, current_average_price=210.00, purchase_date=date(2023, 2, 1)))
    session.add(Investment(code="INV102", portfolio_code="PORT100", asset_type="Stock", ticker="GOOG", quantity=20,
                           purchase_price=300.00, current_average_price=320.00, purchase_date=date(2023, 3, 1)))
    session.add(Investment(code="INV103", portfolio_code="PORT100", asset_type="Bond", ticker="AMZN", quantity=15,
                           purchase_price=200.00, current_average_price=405.00, purchase_date=date(2023, 4, 1)))
    session.add(Investment(code="INV104", portfolio_code="PORT101", asset_type="Stock", ticker="FB", quantity=10,
                           purchase_price=100.00, current_average_price=510.00, purchase_date=date(2023, 5, 1)))
    session.commit()
