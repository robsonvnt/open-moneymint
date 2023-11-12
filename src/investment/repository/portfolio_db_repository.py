from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

from src.investment.domains import PortfolioError, PortfolioModel
from src.investment.helpers import generate_code
from src.investment.repository.db_entities import Portfolio


def to_database(portfolio_model: PortfolioModel) -> Portfolio:
    return Portfolio(
        id=portfolio_model.id,
        code=portfolio_model.code,
        name=portfolio_model.name,
        description=portfolio_model.description
    )


def to_model(portfolio: Portfolio) -> PortfolioModel:
    return PortfolioModel(
        id=portfolio.id,
        code=portfolio.code,
        name=portfolio.name,
        description=portfolio.description
    )


class PortfolioRepo:
    def __init__(self, session):
        self.session = session

    def create(self, new_portfolio: PortfolioModel):
        session = self.session
        try:
            code = generate_code()
            portfolio = Portfolio(
                code=code,
                name=new_portfolio.name,
                description=new_portfolio.description
            )
            session.add(portfolio)
            session.commit()
            session.refresh(portfolio)
            return to_model(portfolio)
        except Exception as e:
            if 'unique constraint' in str(e).lower():
                return PortfolioError.AlreadyExists
            else:
                return PortfolioError.DatabaseError

    def update(self, portfolio_code, updated_portfolio: PortfolioModel):
        session = self.session
        try:
            portfolio = session.query(Portfolio).filter(Portfolio.code == portfolio_code).one()
            portfolio.name = updated_portfolio.name
            portfolio.description = updated_portfolio.description
            session.commit()
            session.refresh(portfolio)
            return to_model(portfolio)
        except NoResultFound as e:
            session.rollback()
            return PortfolioError.PortfolioNotFound
        except SQLAlchemyError as e:
            session.rollback()
            raise e

    def find_all(self):
        session = self.session
        try:
            portfolios = session.query(Portfolio).all()
            return [to_model(portfolio) for portfolio in portfolios]
        except SQLAlchemyError as e:
            session.rollback()
            raise e

    def find_by_code(self, portfolio_code) -> PortfolioModel | PortfolioError:
        session = self.session
        try:
            portfolio = session.query(Portfolio).filter(Portfolio.code == portfolio_code).one()
            return to_model(portfolio)
        except NoResultFound as e:
            session.rollback()
            return PortfolioError.PortfolioNotFound
        except Exception as e:
            session.rollback()
            raise e

    def delete(self, portfolio_code):
        session = self.session
        try:
            portfolio = session.query(Portfolio).filter(Portfolio.code == portfolio_code).one()
            session.delete(portfolio)
            session.commit()
        except (NoResultFound, MultipleResultsFound) as e:
            session.rollback()
            return PortfolioError.PortfolioNotFound
        except SQLAlchemyError as e:
            session.rollback()
            raise e
