import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.auth.domain import UserNotFound, UserModel
from src.auth.repository.user_db_repository import Base, UserRepository, User


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def user_repository(db_session):
    user_repo = UserRepository(db_session)
    return user_repo


def test_create_user(db_session, user_repository):
    user = UserModel(code=None, name="Test User", login="test_login", password="password", created_at=None)
    added_user = user_repository.create(user)
    user_code = added_user.code

    user = db_session.query(User).filter(User.code == user_code).first()
    assert user is not None
    assert user.login == "test_login"


def test_get_user_by_code(db_session, user_repository):
    user = User(name="Test User", code="123", login="test_login", password="password")
    db_session.add(user)
    db_session.commit()

    retrieved_user = user_repository.get_user_by_code("123")
    assert retrieved_user.name == "Test User"
    assert isinstance(retrieved_user, UserModel)

    with pytest.raises(UserNotFound):
        user_repository.get_user_by_code("1233")


def test_get_user_by_login(db_session, user_repository):
    user = User(name="Test User", code="123", login="test_login", password="password")
    db_session.add(user)
    db_session.commit()

    retrieved_user = user_repository.get_user_by_login("test_login")
    assert retrieved_user.name == "Test User"
    assert isinstance(retrieved_user, UserModel)

    with pytest.raises(UserNotFound):
        user_repository.get_user_by_login("1233")


def test_update_user(db_session, user_repository):
    user = User(name="Old Name", code="321", login="old_login", password="old_password")
    db_session.add(user)
    db_session.commit()

    retrieved_user = user_repository.get_user_by_code("321")
    retrieved_user.name = "New Name"
    retrieved_user.login = "new_login"

    updated_user = user_repository.update(user.code, retrieved_user)

    assert updated_user is not None
    assert isinstance(updated_user, UserModel)
    assert updated_user.name == "New Name"
    assert updated_user.login == "new_login"

    with pytest.raises(UserNotFound):
        user_repository.update("1234", updated_user)


def test_delete_user(db_session, user_repository):
    user = User(name="Test User", code="456", login="testuser_login", password="password")
    db_session.add(user)
    db_session.commit()

    user_code = user.code
    user_repository.delete(user_code)

    deleted_user = db_session.query(User).filter(User.code == user_code).first()
    assert deleted_user is None

    with pytest.raises(UserNotFound):
        user_repository.delete("non-existent")
