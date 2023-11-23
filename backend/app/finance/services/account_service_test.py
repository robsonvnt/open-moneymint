import pytest
from unittest.mock import create_autospec

from finance.domain.account_erros import AccountNotFound
from finance.repository.account_repository import AccountRepo
from finance.services.account_service import AccountService
from finance.domain.models import AccountModel


@pytest.fixture
def mock_account_repo():
    return create_autospec(AccountRepo)


@pytest.fixture
def account_service(mock_account_repo):
    return AccountService(mock_account_repo)


def test_create_account(account_service, mock_account_repo):
    mock_data = {"name": "Test Account", "user_code": "USER123", "created_at": "2023-01-01"}
    mock_account_repo.create.return_value = AccountModel(**mock_data)

    result = account_service.create(mock_data)

    mock_account_repo.create.assert_called_once()
    assert result.name == mock_data["name"]


def test_get_account_by_code(account_service, mock_account_repo):
    mock_account_repo.find_by_code.return_value = AccountModel(name="Test Account", user_code="USER123",
                                                               created_at="2023-01-01")

    result = account_service.get_by_code("USER123", "ACC123")

    mock_account_repo.find_by_code.assert_called_once_with("USER123", "ACC123")
    assert result.name == "Test Account"


def test_find_by_code(account_service, mock_account_repo):
    mock_accounts = [
        AccountModel(name="Account 1", user_code="USER123", created_at="2023-01-01"),
        AccountModel(name="Account 2", user_code="USER123", created_at="2023-01-02")
    ]
    mock_account_repo.find_all.return_value = mock_accounts

    results = account_service.get_all_by_user_code("USER123")

    mock_account_repo.find_all.assert_called_once_with("USER123")
    assert len(results) == 2


def test_update_account(account_service, mock_account_repo):
    account: AccountModel = AccountModel(
        name="Updated Account",
        user_code="USER123",
        created_at="2023-01-01"
    )
    mock_account_repo.update.return_value = account

    result = account_service.update("USER123", "ACC123", account)

    mock_account_repo.update.assert_called_once()
    assert result.name == account.name


def test_delete_account(account_service, mock_account_repo):
    mock_account_repo.delete.return_value = True

    result = account_service.delete("USER123", "ACC123")

    mock_account_repo.delete.assert_called_once_with("USER123", "ACC123")
    assert result is True


def test_get_account_by_code_not_found(account_service, mock_account_repo):
    mock_account_repo.find_by_code.side_effect = AccountNotFound()

    with pytest.raises(AccountNotFound):
        account_service.get_by_code("USER123", "NONEXISTENT")
