from typing import List, Optional, Union
from sqlalchemy import Column, Integer, String, Float, Date, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from investment.domains import ConsolidatedPortfolioModel, ConsolidatedBalancePortfolioError

Base = declarative_base()


# Modelo para representar os dados consolidados do portfolio
class ConsolidatedBalancePortfolio(Base):
    __tablename__ = 'consolidated_balance_portfolios'
    id = Column(Integer, primary_key=True)
    portfolio_code = Column(String)
    date = Column(Date)
    balance = Column(Float)
    amount_invested = Column(Float)


# Function to convert domain model to database model
def to_database(cbp_model: ConsolidatedPortfolioModel) -> ConsolidatedBalancePortfolio:
    return ConsolidatedBalancePortfolio(**cbp_model.dict())


# Function to convert database model to domain model
def to_model(cbp: ConsolidatedBalancePortfolio) -> ConsolidatedPortfolioModel:
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
    ) -> Union[List[ConsolidatedPortfolioModel], ConsolidatedBalancePortfolioError]:
        """
        Filters the ConsolidatedBalancePortfolio by date range.
        """
        session = self.session_factory()
        try:
            query = session.query(ConsolidatedBalancePortfolio).filter(
                ConsolidatedBalancePortfolio.portfolio_code == portfolio_code
            )

            if start_date is not None:
                query = query.filter(ConsolidatedBalancePortfolio.date >= start_date)

            if end_date is not None:
                query = query.filter(ConsolidatedBalancePortfolio.date <= end_date)

            query = query.order_by(ConsolidatedBalancePortfolio.date.asc())
            return [to_model(cbp) for cbp in query.all()]
        except SQLAlchemyError as e:
            return ConsolidatedBalancePortfolioError.DatabaseError
        except Exception as e:
            return ConsolidatedBalancePortfolioError.Unexpected
        finally:
            session.close()

    def create(
            self,
            consolidated_portfolio: ConsolidatedPortfolioModel
    ) -> ConsolidatedPortfolioModel | ConsolidatedBalancePortfolioError:
        session = self.session_factory()
        try:
            new_consolidated_portfolio = to_database(consolidated_portfolio)
            session.add(new_consolidated_portfolio)
            session.commit()
            session.refresh(new_consolidated_portfolio)
            return to_model(new_consolidated_portfolio)
        except SQLAlchemyError as e:
            return ConsolidatedBalancePortfolioError.DatabaseError
        except Exception as e:
            return ConsolidatedBalancePortfolioError.Unexpected
        finally:
            session.close()
