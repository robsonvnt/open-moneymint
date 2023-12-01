from datetime import date

from sqlalchemy.exc import NoResultFound
from sqlalchemy import func

from finance.domain.account_erros import AccountNotFound, AccountUnexpectedError
from finance.domain.models import AccountModel
from finance.repository.db.db_entities import Account, FinancialTransaction
from helpers import generate_code


def to_database(account_model: AccountModel) -> Account:
    return Account(**account_model.model_dump())


def to_model(account: Account) -> AccountModel:
    return AccountModel(**account.to_dict())


class AccountRepo:
    def __init__(self, session):
        self.session = session

    def create(self, new_account_data: AccountModel):
        session = self.session
        try:
            code = generate_code()
            new_account = Account(id=None, **new_account_data.model_dump())
            new_account.code = code
            new_account.created_at = date.today()
            session.add(new_account)
            session.commit()
            session.refresh(new_account)
            return to_model(new_account)
        except Exception as e:
            if 'unique constraint' in str(e).lower():
                raise AccountNotFound()
            else:
                raise AccountUnexpectedError()

    def find_by_code(self, user_code: str, account_code: str):
        session = self.session
        try:
            account = session.query(Account).filter(
                Account.code == account_code,
                Account.user_code == user_code
            ).one()
            return to_model(account)
        except NoResultFound:
            raise AccountNotFound()
        except Exception as w:
            raise AccountUnexpectedError()

    def find_all(self, user_code: str):
        session = self.session
        try:
            accounts = session.query(Account).filter(
                Account.user_code == user_code
            ).all()
            return [to_model(account) for account in accounts]
        except Exception as e:
            raise AccountUnexpectedError()

    def delete(self, user_code: str, account_code: str):
        session = self.session
        try:
            account = session.query(Account).filter(
                Account.user_code == user_code,
                Account.code == account_code
            ).one()
            session.delete(account)
            session.commit()
            return True
        except NoResultFound:
            raise AccountNotFound()
        except Exception:
            raise AccountUnexpectedError()

    def update(
            self,
            user_code: str,
            account_code,
            updated_account_data: AccountModel
    ):
        session = self.session
        try:
            account = session.query(Account).filter(
                Account.user_code == user_code,
                Account.code == account_code
            ).one()
            for key, value in updated_account_data.model_dump().items():
                setattr(account, key, value)
            session.commit()
            session.refresh(account)
            return to_model(account)
        except NoResultFound:
            raise AccountNotFound()
        except Exception as e:
            raise AccountUnexpectedError()

    def calculate_balance(self, account_code):
        session = self.session
        query = session.query(
            func.sum(FinancialTransaction.value).label('total_value')
        ).filter(FinancialTransaction.account_code == account_code)
        result = query.one()
        return result.total_value
