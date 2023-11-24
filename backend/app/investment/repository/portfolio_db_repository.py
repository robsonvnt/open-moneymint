from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

from investment.domain.models import PortfolioModel
from investment.domain.portfolio_erros import PortfolioNotFound, PortfolioUnexpectedError
from helpers import generate_code
from investment.repository.db.db_entities import Portfolio


def to_database(portfolio_model: PortfolioModel) -> Portfolio:
    return Portfolio(
        id=portfolio_model.id,
        code=portfolio_model.code,
        name=portfolio_model.name,
        description=portfolio_model.description
    )


def to_model(portfolio: Portfolio) -> PortfolioModel:
    return PortfolioModel(
        code=portfolio.code,
        name=portfolio.name,
        description=portfolio.description,
        user_code=portfolio.user_code
    )


class PortfolioRepo:
    def __init__(self, session):
        self.session = session

    def create(self, user_code: str, new_portfolio: PortfolioModel):
        session = self.session
        try:
            code = generate_code()
            portfolio = Portfolio(
                code=code,
                name=new_portfolio.name,
                description=new_portfolio.description,
                user_code=user_code
            )
            session.add(portfolio)
            session.commit()
            session.refresh(portfolio)
            return to_model(portfolio)
        except Exception as e:
            raise PortfolioUnexpectedError()

    def update(self, user_code: str, portfolio_code, updated_portfolio: PortfolioModel):
        session = self.session
        try:
            portfolio = session.query(Portfolio).filter(
                Portfolio.code == portfolio_code,
                Portfolio.user_code == user_code
            ).one()
            portfolio.name = updated_portfolio.name
            portfolio.description = updated_portfolio.description
            session.commit()
            session.refresh(portfolio)
            return to_model(portfolio)
        except NoResultFound:
            session.rollback()
            raise PortfolioNotFound()
        except SQLAlchemyError:
            session.rollback()
            raise PortfolioUnexpectedError()

    def find_all(self, user_code: str):
        session = self.session
        try:
            portfolios = session.query(Portfolio) \
                .filter(Portfolio.user_code == user_code).all()
            return [to_model(portfolio) for portfolio in portfolios]
        except SQLAlchemyError:
            raise PortfolioUnexpectedError()

    def find_by_code(self, user_code: str, portfolio_code) -> PortfolioModel:
        session = self.session
        try:
            portfolio = session.query(Portfolio).filter(
                Portfolio.code == portfolio_code,
                Portfolio.user_code == user_code
            ).one()
            return to_model(portfolio)
        except NoResultFound as e:
            raise PortfolioNotFound()
        except Exception as e:
            raise PortfolioUnexpectedError()

    def delete(self, user_code: str, portfolio_code):
        session = self.session
        try:
            portfolio = session.query(Portfolio).filter(
                Portfolio.code == portfolio_code,
                Portfolio.user_code == user_code
            ).one()
            session.delete(portfolio)
            session.commit()
        except NoResultFound:
            raise PortfolioNotFound()
        except SQLAlchemyError as e:
            raise PortfolioUnexpectedError()
