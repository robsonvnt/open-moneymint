from unittest.mock import Mock
import tempfile
import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from src.auth.repository.db_connection import get_db_session
from src.auth.repository.user_db_repository import Base


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
def client(db_session):
    def override_get_db():
        yield db_session

    mock_get_price = Mock()
    mock_get_price.return_value.get_price.return_value = 99.99

    from tests.main_test import app
    app.dependency_overrides[get_db_session] = override_get_db
    yield TestClient(app)
