from typing import List

from sqlalchemy.exc import NoResultFound
from datetime import date

from finance.domain.financial_transaction_erros import FinancialTransactionUnexpectedError, FinancialTransactionNotFound
from finance.domain.models import FinancialTransactionModel
from finance.repository.db.db_entities import FinancialTransaction

from helpers import generate_code


def to_database(financial_transaction_model: FinancialTransactionModel) -> FinancialTransaction:
    return FinancialTransaction(**financial_transaction_model.model_dump(exclude_unset=True))


def to_model(financial_transaction: FinancialTransaction) -> FinancialTransactionModel:
    return FinancialTransactionModel(
        **financial_transaction.to_dict(exclude=["id"])
    )


class FinancialTransactionRepo:
    def __init__(self, session):
        self.session = session

    def create(self, new_transaction_data: FinancialTransactionModel) -> FinancialTransactionModel:
        session = self.session
        try:
            new_transaction = FinancialTransaction(
                code=generate_code(),
                **new_transaction_data.model_dump(exclude={'code'})
            )
            session.add(new_transaction)
            session.commit()
            session.refresh(new_transaction)
            return to_model(new_transaction)
        except Exception as e:
            raise FinancialTransactionUnexpectedError()

    def find_by_code(self, transaction_code: str) -> FinancialTransactionModel:
        session = self.session
        try:
            transaction = session.query(FinancialTransaction).filter(
                FinancialTransaction.code == transaction_code
            ).one()
            return to_model(transaction)
        except NoResultFound:
            raise FinancialTransactionNotFound()
        except Exception as e:
            raise FinancialTransactionUnexpectedError()

    def filter_by_account_and_date(
            self,
            account_codes: List[str],
            category_codes: List[str] = None,
            date_start: date = None,
            date_end: date = None
    ) -> List[FinancialTransactionModel]:
        session = self.session
        try:
            query = session.query(FinancialTransaction).filter(
                FinancialTransaction.account_code.in_(account_codes)
            )
            if category_codes:
                query = query.filter(FinancialTransaction.category_code.in_(category_codes))
            if date_start:
                query = query.filter(FinancialTransaction.date >= date_start)
            if date_end:
                query = query.filter(FinancialTransaction.date <= date_end)

            query = query.order_by(FinancialTransaction.id, FinancialTransaction.date)
            transactions = query.all()
            return [to_model(transaction) for transaction in transactions]
        except Exception as e:
            raise FinancialTransactionUnexpectedError()

    def update(self, transaction_code: str,
               updated_transaction_data: FinancialTransactionModel) -> FinancialTransactionModel:
        session = self.session
        try:
            transaction = session.query(FinancialTransaction).filter(
                FinancialTransaction.code == transaction_code
            ).one()
            for key, value in updated_transaction_data.model_dump(exclude={'code', 'account_code'}).items():
                setattr(transaction, key, value if key != "type" else value.value)
            session.commit()
            session.refresh(transaction)
            return to_model(transaction)
        except NoResultFound:
            raise FinancialTransactionNotFound()
        except Exception as e:
            raise FinancialTransactionUnexpectedError()

    def delete(self, transaction_code: str):
        session = self.session
        try:
            transaction = session.query(FinancialTransaction).filter(
                FinancialTransaction.code == transaction_code
            ).one()
            session.delete(transaction)
            session.commit()
        except NoResultFound:
            raise FinancialTransactionNotFound()
        except Exception:
            raise FinancialTransactionUnexpectedError()
