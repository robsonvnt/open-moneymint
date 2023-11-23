from unittest.mock import Mock, patch
import tempfile
import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from auth.user import User, get_current_user
from finance.repository.db.db_connection import get_db_session
from finance.repository.db.db_entities import Account, Base
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

    with patch('investment.repository.factory.RepositoryFactory.create_stock_repo', new=mock_get_price):
        from main_test import app
        app.dependency_overrides[get_db_session] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user

        yield TestClient(app)


def add_accounts(session):
    accounts = [
        Account(code="ACC123", name="Existing Account", description="Description for ACC123", user_code="USER456"),
        Account(code="ACC124", name="Second Account", description="Description for ACC124", user_code="USER457"),
        Account(code="ACC125", name="Other USER456's Account", description="Description for ACC125", user_code="USER456"),
        # Adicione mais contas conforme necessário
    ]

    session.add_all(accounts)
    session.commit()
