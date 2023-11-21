from datetime import date, timedelta

import pytest

from auth.domain.auth_erros import InvalidToken, ExpiredToken
from auth.domain.models import UserModel
from auth.domain.user_erros import UserNotFound
from auth.repository.user_db_repository import UserRepository
from auth.service.services import PasswordService, AuthenticationUserService


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
    secret_key = "secret_key"
    return AuthenticationUserService(mock_user_repository, mock_password_service, secret_key)


@pytest.fixture
def user():
    return UserModel(name="User Test", code="123", user_name="test_login",
                     password="hashed_password", created_at=date.today())


def test_authenticate_user(authentication_user_service, mock_user_repository, mock_password_service, user):
    user_name, password = "test_login", "password"
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


def test_authenticate_user_wrong_password(authentication_user_service, mock_user_repository, mock_password_service,
                                          user):
    user_name, password = "test_login", "password"
    mock_user_repository.get_by_user_name.return_value = user
    mock_password_service.verify_password.return_value = False

    with pytest.raises(UserNotFound):
        authentication_user_service.authenticate_user(user_name, password)


def test_create_access_token(authentication_user_service, user):
    time_delta = timedelta(days=1)
    token = authentication_user_service.create_access_token(user, time_delta)
    assert isinstance(token, str)
    assert len(token) > 0


def test_get_username_from_access_token(authentication_user_service, user):
    time_delta = timedelta(days=1)
    token = authentication_user_service.create_access_token(user, time_delta)

    result = authentication_user_service.get_username_from_access_token(token)
    assert result == user.user_name


def test_get_username_from_access_token_invalid_token(authentication_user_service, user):
    user = UserModel(name="User Test", code="123", user_name="test_login",
                     password="hashed_password", created_at=date.today())
    time_delta = timedelta(days=1)
    token = authentication_user_service.create_access_token(user, time_delta)

    other_sk_auth_service = AuthenticationUserService(mock_user_repository, mock_password_service, "other_secret_key")

    with pytest.raises(InvalidToken):
        other_sk_auth_service.get_username_from_access_token(token)


def test_get_username_from_access_token_expired_token(authentication_user_service, user):
    user = UserModel(name="User Test", code="123", user_name="test_login",
                     password="hashed_password", created_at=date.today())
    time_delta = timedelta(days=-1)
    token = authentication_user_service.create_access_token(user, time_delta)

    with pytest.raises(ExpiredToken):
        authentication_user_service.get_username_from_access_token(token)
