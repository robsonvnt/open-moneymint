from datetime import date
from typing import List

from sqlalchemy.exc import NoResultFound

from finance.domain.account_erros import AccountConsolidationNotFound, AccountConsolidationAlreadyExists
from finance.domain.models import AccountConsolidationModel
from finance.repository.db.db_entities import AccountConsolidation
from helpers import get_last_day_of_the_month


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
        except Exception as e:
            raise AccountConsolidationAlreadyExists()

    def find_by_account_month(self, account_codes: List[str], month: date):
        session = self.session
        try:
            consolidations = session.query(AccountConsolidation).filter(
                AccountConsolidation.account_code.in_(account_codes),
                AccountConsolidation.month == date(month.year, month.month, 1)
            ).all()
            return [to_model(consolidation) for consolidation in consolidations]
        except NoResultFound:
            raise AccountConsolidationNotFound()

    def find_all_by_account(self, account_codes: List[str], start_month: date = None, end_month: date = None):
        session = self.session
        query = session.query(AccountConsolidation).filter(
            AccountConsolidation.account_code.in_(account_codes)
        )
        if start_month:
            query = query.filter(AccountConsolidation.month >= date(start_month.year, start_month.month, 1))
        if end_month:
            query = query.filter(AccountConsolidation.month <= get_last_day_of_the_month(end_month))
        consolidations = query.all()
        return [to_model(consolidation) for consolidation in consolidations]

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
