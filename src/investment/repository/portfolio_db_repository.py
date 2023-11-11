from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

from src.investment.domains import PortfolioError, PortfolioModel
from src.investment.helpers import generate_code

Base = declarative_base()


class Portfolio(Base):
    __tablename__ = 'portfolios'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)


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
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create(self, new_portfolio: PortfolioModel):
        session = self.Session()
        try:
            code = generate_code()
            portfolio = Portfolio(
                code=code, name=new_portfolio.name, description=new_portfolio.description
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
        finally:
            session.close()

    def update(self, portfolio_code, updated_portfolio: PortfolioModel):
        session = self.Session()
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
        finally:
            session.close()

    def find_all(self):
        session = self.Session()
        try:
            portfolios = session.query(Portfolio).all()
            return [to_model(portfolio) for portfolio in portfolios]
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def find_by_code(self, portfolio_code) -> PortfolioModel:
        session = self.Session()
        try:
            portfolio = session.query(Portfolio).filter(Portfolio.code == portfolio_code).one()
            return to_model(portfolio)
        except NoResultFound as e:
            session.rollback()
            return PortfolioError.PortfolioNotFound
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete(self, portfolio_code):
        session = self.Session()
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
        finally:
            session.close()
