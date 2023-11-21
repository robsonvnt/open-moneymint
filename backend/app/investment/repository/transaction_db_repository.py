from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound
from investment.domain.models import TransactionModel
from investment.domain.transaction_errors import TransactionNotFound, TransactionUnexpectedError
from investment.helpers import generate_code
from investment.repository.db.db_entities import Transaction
from investment.repository.investment_db_repository import InvestmentRepo


def to_database(transaction_model: TransactionModel) -> Transaction:
    return Transaction(
        id=None,
        code=transaction_model.code,
        investment_code=transaction_model.investment_code,
        type=transaction_model.type,
        date=transaction_model.date,
        quantity=transaction_model.quantity,
        price=transaction_model.price
    )


def to_model(transaction: Transaction) -> TransactionModel:
    return TransactionModel(
        code=transaction.code,
        investment_code=transaction.investment_code,
        type=transaction.type,
        date=transaction.date,
        quantity=transaction.quantity,
        price=transaction.price
    )


class TransactionRepo:
    def __init__(self, session):
        self.session = session

    def create(self, new_transaction: TransactionModel):
        session = self.session
        try:
            code = new_transaction.code if new_transaction.code else generate_code()
            transaction = Transaction(
                code=code,
                investment_code=new_transaction.investment_code,
                type=new_transaction.type.value,
                date=new_transaction.date,
                quantity=new_transaction.quantity,
                price=new_transaction.price
            )
            session.add(transaction)
            session.commit()
            session.refresh(transaction)
            return to_model(transaction)
        except Exception:
            session.rollback()
            raise TransactionUnexpectedError()

    def update(self, transaction_code, updated_transaction_model: TransactionModel):
        session = self.session
        try:
            transaction = session.query(Transaction).filter(Transaction.code == transaction_code).one()

            transaction.investment_code = updated_transaction_model.investment_code
            transaction.type = updated_transaction_model.type.value
            transaction.date = updated_transaction_model.date
            transaction.quantity = updated_transaction_model.quantity
            transaction.price = updated_transaction_model.price

            session.commit()
            session.refresh(transaction)
            return to_model(transaction)
        except NoResultFound as e:
            session.rollback()
            raise TransactionNotFound()
        except SQLAlchemyError as e:
            session.rollback()
            raise TransactionUnexpectedError()

    def find_all(self, portfolio_code, investment_code):
        session = self.session
        try:
            inv = InvestmentRepo(session).find_by_portf_investment_code(portfolio_code, investment_code)
            transactions = session.query(Transaction).filter(
                Transaction.investment_code == inv.code,
            ).order_by(Transaction.date.desc()).all()
            return [to_model(transaction) for transaction in transactions]
        except NoResultFound:
            return []
        except SQLAlchemyError:
            raise TransactionUnexpectedError()

    def find_by_code(self, transaction_code) -> TransactionModel:
        session = self.session
        try:
            transaction = session.query(Transaction).filter(Transaction.code == transaction_code).one()
            return to_model(transaction)
        except NoResultFound as e:
            raise TransactionNotFound()
        except SQLAlchemyError as e:
            raise TransactionUnexpectedError()

    def delete(self, transaction_code):
        session = self.session
        try:
            transaction = session.query(Transaction).filter(Transaction.code == transaction_code).one()
            session.delete(transaction)
            session.commit()
        except (NoResultFound, MultipleResultsFound) as e:
            session.rollback()
            raise TransactionNotFound()
        except SQLAlchemyError as e:
            session.rollback()
            raise TransactionUnexpectedError()
