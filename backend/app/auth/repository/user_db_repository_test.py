import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from auth.domain.models import UserModel
from auth.domain.user_erros import UserNotFound
from auth.repository.user_db_repository import Base, UserRepository, User


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
    user = UserModel(code=None, name="Test User", user_name="test_user_name", password="password", created_at=None)
    added_user = user_repository.create(user)
    user_code = added_user.code

    user = db_session.query(User).filter(User.code == user_code).first()
    assert user is not None
    assert user.user_name == "test_user_name"


def test_get_user_by_code(db_session, user_repository):
    user = User(name="Test User", code="123", user_name="test_user_name", password="password")
    db_session.add(user)
    db_session.commit()

    retrieved_user = user_repository.get_user_by_code("123")
    assert retrieved_user.name == "Test User"
    assert isinstance(retrieved_user, UserModel)

    with pytest.raises(UserNotFound):
        user_repository.get_user_by_code("1233")


def test_get_user_by_user_name(db_session, user_repository):
    user = User(name="Test User", code="123", user_name="test_user_name", password="password")
    db_session.add(user)
    db_session.commit()

    retrieved_user = user_repository.get_by_user_name("test_user_name")
    assert retrieved_user.name == "Test User"
    assert isinstance(retrieved_user, UserModel)

    with pytest.raises(UserNotFound):
        user_repository.get_by_user_name("1233")


def test_update_user(db_session, user_repository):
    user = User(name="Old Name", code="321", user_name="old_user_name", password="old_password")
    db_session.add(user)
    db_session.commit()

    retrieved_user = user_repository.get_user_by_code("321")
    retrieved_user.name = "New Name"
    retrieved_user.user_name = "new_user_name"

    updated_user = user_repository.update(user.code, retrieved_user)

    assert updated_user is not None
    assert isinstance(updated_user, UserModel)
    assert updated_user.name == "New Name"
    assert updated_user.user_name == "new_user_name"

    with pytest.raises(UserNotFound):
        user_repository.update("1234", updated_user)


def test_delete_user(db_session, user_repository):
    user = User(name="Test User", code="456", user_name="testuser_user_name", password="password")
    db_session.add(user)
    db_session.commit()

    user_code = user.code
    user_repository.delete(user_code)

    deleted_user = db_session.query(User).filter(User.code == user_code).first()
    assert deleted_user is None

    with pytest.raises(UserNotFound):
        user_repository.delete("non-existent")
