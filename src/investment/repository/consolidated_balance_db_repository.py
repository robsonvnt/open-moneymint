from datetime import date
from typing import List, Optional, Union
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from src.investment.domains import ConsolidatedPortfolioModel, ConsolidatedPortfolioError

Base = declarative_base()


# Modelo para representar os dados consolidados do portfolio
class ConsolidatedPortfolio(Base):
    __tablename__ = 'consolidated_balance_portfolios'
    id = Column(Integer, primary_key=True)
    portfolio_code = Column(String)
    date = Column(Date)
    balance = Column(Float)
    amount_invested = Column(Float)


# Function to convert domain model to database model
def to_database(cbp_model: ConsolidatedPortfolioModel) -> ConsolidatedPortfolio:
    return ConsolidatedPortfolio(id=None, **cbp_model.dict())


# Function to convert database model to domain model
def to_model(cbp: ConsolidatedPortfolio) -> ConsolidatedPortfolioModel:
    return ConsolidatedPortfolioModel(**cbp.__dict__)


# Repositório para interagir com a tabela consolidated_balance_portfolios
class ConsolidatedBalanceRepo:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def filter_by_date_range(
            self,
            portfolio_code: str,
            start_date: Optional[Date] = None,
            end_date: Optional[Date] = None
    ) -> Union[List[ConsolidatedPortfolioModel], ConsolidatedPortfolioError]:
        """
        Filters the ConsolidatedBalancePortfolio by date range.
        """
        session = self.session_factory()
        try:
            query = session.query(ConsolidatedPortfolio).filter(
                ConsolidatedPortfolio.portfolio_code == portfolio_code
            )

            if start_date is not None:
                query = query.filter(ConsolidatedPortfolio.date >= start_date)

            if end_date is not None:
                query = query.filter(ConsolidatedPortfolio.date <= end_date)

            query = query.order_by(ConsolidatedPortfolio.date.asc())
            return [to_model(cbp) for cbp in query.all()]
        except SQLAlchemyError as e:
            return ConsolidatedPortfolioError.DatabaseError
        except Exception as e:
            return ConsolidatedPortfolioError.Unexpected
        finally:
            session.close()

    def __get_consolidated_portfolio(
            self, session, portfolio_code: str, date: date
    ) -> ConsolidatedPortfolio | ConsolidatedPortfolioError:
        try:
            consolidated_portfolio = session.query(ConsolidatedPortfolio) \
                .filter(ConsolidatedPortfolio.date == date) \
                .filter(ConsolidatedPortfolio.portfolio_code == portfolio_code) \
                .one()
            return consolidated_portfolio
        except NoResultFound:
            return ConsolidatedPortfolioError.ConsolidatedPortfolioNotFound
        except Exception as e:
            return ConsolidatedPortfolioError.DatabaseError

    def create_or_update(
            self,
            cpm: ConsolidatedPortfolioModel
    ) -> ConsolidatedPortfolioModel | ConsolidatedPortfolioError:
        session = self.session_factory()
        try:
            result = self.__get_consolidated_portfolio(session, cpm.portfolio_code, date.today())
            match result:
                case ConsolidatedPortfolio():
                    consolidated_portfolio = result
                    consolidated_portfolio.balance = cpm.balance
                    consolidated_portfolio.amount_invested = cpm.amount_invested
                    session.refresh(consolidated_portfolio)
                    return to_model(consolidated_portfolio)
                case ConsolidatedPortfolioError.ConsolidatedPortfolioNotFound:
                    consolidated_portfolio = to_database(cpm)
                    session.add(consolidated_portfolio)
                    to_model(consolidated_portfolio)
                    return to_model(consolidated_portfolio)
                case _:
                    return ConsolidatedPortfolioError.Unexpected
        except SQLAlchemyError as e:
            return ConsolidatedPortfolioError.DatabaseError
        except Exception as e:
            return ConsolidatedPortfolioError.Unexpected
        finally:
            session.commit()
            session.close()
