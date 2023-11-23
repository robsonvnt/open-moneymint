from finance.domain.models import AccountModel

from finance.repository.account_repository import AccountRepo


class AccountService:
    def __init__(self, account_repo: AccountRepo):
        self.account_repo = account_repo

    def create(self, new_account: AccountModel) -> AccountModel:
        return self.account_repo.create(new_account)

    def get_by_code(self, user_code: str, account_code: str) -> AccountModel:
        return self.account_repo.find_by_code(user_code, account_code)

    def get_all_by_user_code(self, user_code: str) -> list[AccountModel]:
        return self.account_repo.find_all(user_code)

    def update(self, user_code: str, account_code: str, updated_account: AccountModel) -> AccountModel:
        return self.account_repo.update(user_code, account_code, updated_account)

    def delete(self, user_code: str, account_code: str) -> bool:
        return self.account_repo.delete(user_code, account_code)
