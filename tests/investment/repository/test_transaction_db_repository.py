from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from src.investment.domains import TransactionModel, TransactionType, TransactionError
from src.investment.repository.db.db_entities import Base, Transaction
from src.investment.repository.transaction_db_repository import TransactionRepo


# Configuração do banco de dados de teste
@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


# Teste para o método create
def test_create_transaction(session):
    repo = TransactionRepo(session)
    new_transaction = TransactionModel(
        code=None,
        investment_code="INV101",
        type=TransactionType.BUY,
        date=date.today(),
        quantity=15,
        price=33.5,
    )
    created_portfolio = repo.create(new_transaction)

    assert created_portfolio is not None
    assert len(created_portfolio.code) == 10

    try:
        session.query(Transaction).filter(Transaction.code == created_portfolio.code).one()
        assert True
    except:
        assert False


def test_update_transaction_success(session):
    # Configuração inicial: cria uma transação para teste
    repo = TransactionRepo(session)
    initial_transaction = TransactionModel(
        code=None,
        investment_code="INV001",
        type=TransactionType.BUY,
        date=date.today(),
        quantity=10,
        price=100.0
    )
    transaction = repo.create(initial_transaction)

    # Dados de atualização
    updated_transaction = TransactionModel(
        code=transaction.code,
        investment_code="INV001",
        type=TransactionType.BUY,
        date=date.today(),
        quantity=5,
        price=150.0
    )

    # Teste de atualização
    result = repo.update(transaction.code, updated_transaction)
    assert result is not None
    assert result.quantity == 5
    assert result.price == 150.0


def test_update_transaction_not_found(session):
    # Configuração inicial: repositório sem transações
    repo = TransactionRepo(session)

    # Tentativa de atualizar uma transação inexistente
    updated_transaction = TransactionModel(
        code=None,
        investment_code="INV002",
        type=TransactionType.BUY,
        date=date.today(),
        quantity=20,
        price=200.0
    )

    # Teste para transação não encontrada
    result = repo.update("NON_EXISTENT_CODE", updated_transaction)
    assert result == TransactionError.TransactionNotFound


def test_find_all_from_investment_code(session):
    repo = TransactionRepo(session)

    # Criando transações de teste
    for i in range(4):
        transaction = TransactionModel(
            code=None,
            investment_code="INV123" if i != 2 else "INV321",
            type=TransactionType.BUY,
            date=date.today(),
            quantity=10 + i,
            price=100.0 + i
        )
        repo.create(transaction)

    # Testando a busca por todas as transações para um código de investimento específico
    transactions = repo.find_all_from_investment_code("INV123")
    assert len(transactions) == 3
    assert all(t.investment_code == "INV123" for t in transactions)


def test_find_by_code_success(session):
    repo = TransactionRepo(session)
    transaction = TransactionModel(
        code=None,
        investment_code="INV123",
        type=TransactionType.BUY,
        date=date.today(),
        quantity=10,
        price=100.0
    )
    created_transaction = repo.create(transaction)

    # Testando a busca por uma transação específica
    found_transaction = repo.find_by_code(created_transaction.code)
    assert found_transaction is not None
    assert found_transaction.code == created_transaction.code


def test_find_by_code_not_found(session):
    repo = TransactionRepo(session)

    # Testando a busca por uma transação inexistente
    result = repo.find_by_code("NON_EXISTENT_CODE")
    assert result == TransactionError.TransactionNotFound
