import pytest

from auth.domain.models import UserModel
from auth.domain.user_erros import UserNotFound
from auth.repository.user_db_repository import UserRepository
from auth.service.services import UserService, PasswordService


@pytest.fixture
def mock_user_repository(mocker):
    mock_repo = mocker.Mock(UserRepository)
    mock_repo.create.side_effect = lambda user: user
    return mock_repo


@pytest.fixture
def mock_password_service(mocker):
    mock = mocker.Mock(PasswordService)
    mock.protect_password.return_value = "hashed_password"
    return mock


@pytest.fixture
def user_service(mock_user_repository, mock_password_service):
    return UserService(mock_user_repository, mock_password_service)


def test_create_user(user_service, mock_user_repository):
    user = UserModel(name="Test", code="123", user_name="test_login", password="password", created_at=None)
    created_user = user_service.create(user)

    mock_user_repository.create.assert_called_once()
    assert created_user.password == "hashed_password"


def test_get_user_by_code_found(user_service, mock_user_repository):
    mock_user_repository.get_user_by_code.return_value = UserModel(name="Test", code="123", user_name="test_login",
                                                                   password="password", created_at=None)
    user = user_service.get_user_by_code("123")
    assert user.code == "123"
    mock_user_repository.get_user_by_code.assert_called_once_with("123")


def test_get_user_by_code_not_found(user_service, mock_user_repository):
    mock_user_repository.get_user_by_code.side_effect = UserNotFound()
    with pytest.raises(UserNotFound):
        user_service.get_user_by_code("123")


def test_update_user(user_service, mock_user_repository):
    updated_user = UserModel(name="Updated", code="123", user_name="test_login",
                             password="password", created_at=None)
    mock_user_repository.update.return_value = updated_user

    result = user_service.update(updated_user)
    mock_user_repository.update.assert_called_once()
    assert result.name == "Updated"


def test_update_user_not_found(user_service, mock_user_repository):
    updated_user = UserModel(name="Updated", code="123", user_name="test_login",
                             password="password", created_at=None)
    mock_user_repository.update.side_effect = UserNotFound()

    with pytest.raises(UserNotFound):
        user_service.update(updated_user)


def test_delete_user(user_service, mock_user_repository):
    user_service.delete("123")
    mock_user_repository.delete.assert_called_once()


def test_delete_user_not_found(user_service, mock_user_repository):
    mock_user_repository.delete.side_effect = UserNotFound()

    with pytest.raises(UserNotFound):
        user_service.delete("123")
