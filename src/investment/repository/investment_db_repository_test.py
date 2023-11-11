import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.investment.domains import InvestmentError
from src.investment.repository.db_entities import Base
from src.investment.repository.investment_db_repository import InvestmentRepo, Investment

engine = create_engine('sqlite:///:memory:')  # Banco de dados SQLite em memória
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def investment_repo():
    return InvestmentRepo(session_factory=TestingSessionLocal)


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


def test_find_all_by_portfolio_code_with_data(db_session, investment_repo):
    """
    Testa se a função retorna os investimentos corretos para um dado código de portfólio.
    """
    # Adicionar dados de teste
    add_investments(db_session)
    db_session.commit()

    results = investment_repo.find_all_by_portfolio_code("PORT100")
    assert len(results) == 4
    assert results[0].ticker == "AAPL"
    assert results[1].ticker == "MSFT"


def test_find_all_by_portfolio_code_with_order_by(db_session, investment_repo):
    """
    Testa se a função retorna os investimentos corretos e ordenados por purchase_price para um dado código de portfólio.
    """
    # Adicionar dados de teste
    add_investments(db_session)
    db_session.commit()

    results = investment_repo.find_all_by_portfolio_code("PORT100", order_by="purchase_price")
    assert results[0].code == "INV103"
    assert results[3].code == "INV100"

    # Testando em ordem decrescente
    results = investment_repo.find_all_by_portfolio_code("PORT100", order_by="purchase_price.desc")
    assert results[0].code == "INV100"
    assert results[3].code == "INV103"

def test_find_all_by_portfolio_code_with_order_by_non_existent_column(db_session, investment_repo):
    """
    Testa se a função retorna erro por não existir a coluna a src ordenada.
    """
    # Adicionar dados de teste
    add_investments(db_session)
    db_session.commit()

    results = investment_repo.find_all_by_portfolio_code("PORT100", order_by="non-existent column")
    assert results == InvestmentError.ColumnDoesNotExist

def test_find_all_by_portfolio_code_empty(db_session, investment_repo):
    """
    Testa se a função retorna uma lista vazia quando não há investimentos correspondentes.
    """
    results = investment_repo.find_all_by_portfolio_code("PORT100")
    assert results == []
    assert len(results) == 0
