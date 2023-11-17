from datetime import date

import pytest

from src.auth.domain import UserModel, UserNotFound
from src.auth.repository.user_db_repository import UserRepository
from src.auth.services import PasswordService, AuthenticationUserService


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
def authentication_user_service(mock_user_repository, mock_password_service):
    return AuthenticationUserService(mock_user_repository, mock_password_service)


def test_authenticate_user(authentication_user_service, mock_user_repository, mock_password_service):
    user_name, password = "test_login", "password"
    user = UserModel(name="User Test", code="123", user_name="test_login",
                     password="hashed_password", created_at=date.today())
    mock_user_repository.get_by_user_name.return_value = user
    mock_password_service.verify_password.return_value = True

    # Chamada a ser testada
    logged_user = authentication_user_service.authenticate_user(user_name, password)

    # Testa se chamou o get_user_by_login uma vez
    mock_user_repository.get_by_user_name.assert_called_once_with(user_name)
    # Testa se chamou o verify_password com a senha do parametro e a senha do user do DB
    mock_password_service.verify_password.assert_called_once_with(password, user.password)
    assert logged_user.user_name == user_name
    assert user.user_name == user_name


def test_authenticate_user_not_found(authentication_user_service, mock_user_repository, mock_password_service):
    user_name, password = "test_login", "password"
    mock_user_repository.get_by_user_name.side_effect = UserNotFound()
    mock_password_service.verify_password.return_value = True

    with pytest.raises(UserNotFound):
        authentication_user_service.authenticate_user(user_name, password)


def test_authenticate_user_wrong_password(authentication_user_service, mock_user_repository, mock_password_service):
    user_name, password = "test_login", "password"
    user = UserModel(name="User Test", code="123", user_name="test_login",
                     password="hashed_password", created_at=date.today())
    mock_user_repository.get_by_user_name.return_value = user
    mock_password_service.verify_password.return_value = False

    with pytest.raises(UserNotFound):
        authentication_user_service.authenticate_user(user_name, password)
