from typing import List, Optional
from sqlalchemy import Column, Integer, String, Float, Date, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from investment.domains import ConsolidatedBalancePortfolioModel, ConsolidatedBalancePortfolioError

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
def to_database(cbp_model: ConsolidatedBalancePortfolioModel) -> ConsolidatedBalancePortfolio:
    return ConsolidatedBalancePortfolio(**cbp_model.dict())


# Function to convert database model to domain model
def to_model(cbp: ConsolidatedBalancePortfolio) -> ConsolidatedBalancePortfolioModel:
    return ConsolidatedBalancePortfolioModel(**cbp.__dict__)


# Repositório para interagir com a tabela consolidated_balance_portfolios
class ConsolidatedBalanceRepo:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def filter_by_date_range(
            self,
            portfolio_code: str,
            start_date: Optional[Date] = None,
            end_date: Optional[Date] = None
    ) -> List[ConsolidatedBalancePortfolioModel]:
        """
        Filters the ConsolidatedBalancePortfolio by date range.
        """
        try:
            query = self.session.query(ConsolidatedBalancePortfolio).filter(
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
