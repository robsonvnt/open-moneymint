from finance.domain.account_erros import AccountNotFound
from finance.domain.models import AccountModel
from finance.repository.account_repository import AccountRepo
from finance.repository.db.prepare_to_db_test import *


def test_create_account(memory_db_session):
    """
    Testa se a função de criação de conta está funcionando corretamente.
    """
    account_repo = AccountRepo(memory_db_session)
    new_account_data = AccountModel(
        name="Test Account",
        user_code="USER123",
    )

    account_model = account_repo.create(new_account_data)
    assert len(account_model.code) == 10
    assert account_model.name == "Test Account"
    assert account_model.user_code == "USER123"
    assert account_model.created_at == date.today()


def test_find_by_code(memory_db_session):
    """
    Testa se a função encontra a conta correta pelo código.
    """
    add_accounts(memory_db_session)
    account_repo = AccountRepo(memory_db_session)

    account_model = account_repo.find_by_code("USER001", "ACC123")
    assert account_model.name == "Existing Account"
    assert account_model.user_code == "USER001"

    with pytest.raises(AccountNotFound):
        account_repo.find_by_code("USER001", "NONEXISTENT")


def test_delete_account(memory_db_session):
    """
    Testa se a função de exclusão de conta está funcionando corretamente.
    """
    add_accounts(memory_db_session)
    account_repo = AccountRepo(memory_db_session)

    result = account_repo.delete("USER001", "ACC123")
    assert result is True

    with pytest.raises(AccountNotFound):
        account_repo.delete("USER001", "NONEXISTENT")


def test_update_account(memory_db_session):
    """
    Testa se a função de atualização de conta está funcionando corretamente.
    """
    add_accounts(memory_db_session)
    account_repo = AccountRepo(memory_db_session)
    updated_account_data = AccountModel(name="Updated Account", user_code="USER789")

    updated_account_model = account_repo.update("USER001", "ACC123", updated_account_data)
    assert updated_account_model.name == "Updated Account"
    assert updated_account_model.user_code == "USER789"

    with pytest.raises(AccountNotFound):
        account_repo.update("PORT123", "NONEXISTENT", updated_account_data)


def test_find_all_by_user_code(memory_db_session):
    """
    Testa se a função find_all retorna todas as contas associadas a um user_code específico.
    """
    # Adiciona contas de teste ao banco de dados
    add_accounts(memory_db_session)

    account_repo = AccountRepo(memory_db_session)

    # Testa o retorno de todas as contas para um user_code específico
    user_code_test = "USER001"
    accounts = account_repo.find_all(user_code_test)
    assert len(accounts) == 2
    for account in accounts:
        assert account.user_code == user_code_test

    # Testa o retorno de contas para um user_code que não existe
    accounts = account_repo.find_all("NONEXISTENT_USER")
    assert len(accounts) == 0


def test_calculate_balance(memory_db_session):
    add_accounts(memory_db_session)
    add_transactions(memory_db_session)
    account_repo = AccountRepo(memory_db_session)

    result = account_repo.calculate_balance("ACC123")

     # Saldo deve ser 0
    assert result == 0
