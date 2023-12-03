from datetime import date

from sqlalchemy.exc import NoResultFound

from finance.domain.account_erros import AccountConsolidationNotFound, AccountConsolidationAlreadyExists
from finance.domain.models import AccountConsolidationModel
from finance.repository.db.db_entities import AccountConsolidation


def to_database(consolidation_model: AccountConsolidationModel) -> AccountConsolidation:
    return AccountConsolidation(**consolidation_model.model_dump())


def to_model(account: AccountConsolidation) -> AccountConsolidationModel:
    return AccountConsolidationModel(**account.to_dict())


class AccountConsolidationRepo:
    def __init__(self, session):
        self.session = session

    def create(self, new_consolidation_data: AccountConsolidationModel):
        session = self.session
        try:
            new_account = AccountConsolidation(**new_consolidation_data.model_dump())
            session.add(new_account)
            session.commit()
            session.refresh(new_account)
            return to_model(new_account)
        except NoResultFound:
            raise AccountConsolidationAlreadyExists()

    def find_by_account_month(self, account_code: str, month: date):
        session = self.session
        try:
            consolidations = session.query(AccountConsolidation).filter(
                AccountConsolidation.account_code == account_code,
                AccountConsolidation.month == date(month.year, month.month, 1)
            ).one()
            return to_model(consolidations)
        except NoResultFound:
            raise AccountConsolidationNotFound()

    def find_all_by_account(self, account_code: str):
        session = self.session
        accounts = session.query(AccountConsolidation).filter(
            AccountConsolidation.account_code == account_code
        ).all()
        return [to_model(account) for account in accounts]

    def update(
            self,
            updated_consolidation_data: AccountConsolidationModel
    ):
        session = self.session
        try:
            account = session.query(AccountConsolidation).filter(
                AccountConsolidation.account_code == updated_consolidation_data.account_code,
                AccountConsolidation.month == updated_consolidation_data.month
            ).one()
            account.balance = updated_consolidation_data.balance
            session.commit()
            session.refresh(account)
            return to_model(account)
        except NoResultFound:
            raise AccountConsolidationNotFound()
