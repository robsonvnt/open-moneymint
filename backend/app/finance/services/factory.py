from finance.repository.account_repository import AccountRepo
from finance.services.account_service import AccountService


class ServiceFactory:
    @staticmethod
    def create_account_service(session=None) -> AccountService:
        account_repo = AccountRepo(session)
        return AccountService(account_repo)
