from datetime import date
from unittest.mock import Mock, patch
import tempfile
import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from auth.user import User, get_current_user
from finance.domain.models import TransactionType
from finance.repository.db.db_connection import get_db_session
from finance.repository.db.db_entities import Account, Base, Category, FinancialTransaction
from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def db_session():
    db_file = tempfile.NamedTemporaryFile(suffix='.sqlite', delete=False)
    db_file_path = db_file.name
    db_file.close()

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
def memory_db_session():
    db_file = tempfile.NamedTemporaryFile(suffix='.sqlite', delete=False)
    db_file_path = db_file.name
    db_file.close()

    engine = create_engine(f"sqlite:///:memory:", connect_args={"check_same_thread": False})
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
        return User(name="test", user_name="test", code="USER001")

    mock_get_price = Mock()
    mock_get_price.return_value.get_price.return_value = 99.99

    with patch('investment.repository.factory.RepositoryFactory.create_stock_repo', new=mock_get_price):
        from main_test import app
        app.dependency_overrides[get_db_session] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user

        yield TestClient(app)


def add_accounts(session):
    accounts = [
        Account(code="ACC123", name="Existing Account", description="Description for ACC123", user_code="USER001"),
        Account(code="ACC124", name="Second Account", description="Description for ACC124", user_code="USER002"),
        Account(code="ACC125", name="Other USER456's Account", description="Description for ACC125",
                user_code="USER001"),
        # Adicione mais contas conforme necessário
    ]
    session.add_all(accounts)
    session.commit()


def add_transactions(session):
    transactions = [
        FinancialTransaction(
            code="TRA001", account_code="ACC123", description="Description 1", category_code="CAT001",
            type=TransactionType.TRANSFER.value, date=date(2023, 5, 5), value=100.0
        ),
        FinancialTransaction(
            code="TRA002", account_code="ACC123", description="Description 2", category_code="CAT003",
            type=TransactionType.DEPOSIT.value, date=date(2023, 5, 10), value=200.0
        ),
        FinancialTransaction(
            code="TRA003", account_code="ACC123", description="Description 3", category_code="CAT003",
            type=TransactionType.TRANSFER.value, date=date(2023, 6, 5), value=300.0
        ),
        FinancialTransaction(
            code="TRA004", account_code="ACC124", description="Description 4", category_code="CAT004",
            type=TransactionType.TRANSFER.value, date=date(2023, 5, 5), value=150.0
        ),
        FinancialTransaction(
            code="TRA005", account_code="ACC124", description="Description 5", category_code="CAT005",
            type=TransactionType.TRANSFER.value, date=date(2023, 4, 5), value=250.0
        ),
        FinancialTransaction(
            code="TRA006", account_code="ACC125", description="Description 6", category_code="CAT003",
            type=TransactionType.TRANSFER.value, date=date(2023, 5, 5), value=250.0
        )
    ]
    session.add_all(transactions)
    session.commit()


def add_categories(session):
    categories = []
    categories.append(Category(
        code="CAT001",
        name="Main Category",
        user_code="USER001",
        parent_category_code=None,
        created_at=date.today()
    ))
    # Adds child categories to category 001
    for i in range(2, 5):
        categories.append(
            Category(
                code=f"CAT00{i}",
                name=f"Child Category {i}",
                user_code="USER001",
                parent_category_code="CAT001",
                created_at=date.today()
            )
        )
    # Adds 3 another USER001 categories without parent
    for i in range(5, 8):
        categories.append(
            Category(
                code=f"CAT00{i}",
                name=f"Child Category {i}",
                user_code="USER001",
                parent_category_code=None,
                created_at=date.today()
            )
        )
    # Adds child categories to category 003
    for i in range(8, 12):
        categories.append(
            Category(
                code=f"CAT00{i}",
                name=f"Child Category {i}",
                user_code="USER001",
                parent_category_code="CAT003",
                created_at=date.today()
            )
        )

    # Adds 3 another categories without parent and USER002
    for i in range(12, 15):
        categories.append(
            Category(
                code=f"CAT00{i}",
                name=f"Child Category {i}",
                user_code="USER002",
                parent_category_code=None,
                created_at=date.today()
            )
        )
    session.add_all(categories)
    session.commit()
