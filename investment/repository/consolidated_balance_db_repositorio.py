from sqlalchemy import Column, Integer, String, Float, Date, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_mixins import AllFeaturesMixin

from investment.domains import ConsolidatedBalancePortfolioModel, ConsolidatedBalancePortfolioError

Base = declarative_base()


# Modelo para representar os dados consolidados do portfolio
class ConsolidatedBalancePortfolio(Base, AllFeaturesMixin):
    __tablename__ = 'consolidated_balance_portfolios'
    id = Column(Integer, primary_key=True)
    portfolio_code = Column(String)
    date = Column(Date)
    balance = Column(Float)
    amount_invested = Column(Float)


def to_database(cbp_model: ConsolidatedBalancePortfolioModel) -> ConsolidatedBalancePortfolio:
    return ConsolidatedBalancePortfolio(**cbp_model.model_dump())


def to_model(cbp: ConsolidatedBalancePortfolio) -> ConsolidatedBalancePortfolioModel:
    return ConsolidatedBalancePortfolioModel(**cbp.to_dict())


# Repositório para interagir com a tabela consolidated_balance_portfolios
class ConsolidatedBalanceRepo:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def filter_by_date_range(self, portfolio_code, start_date=None, end_date=None):
        try:
            query = self.session.query(ConsolidatedBalancePortfolio).filter(
                ConsolidatedBalancePortfolio.portfolio_code == portfolio_code
            )

            if start_date is not None:
                query = query.filter(ConsolidatedBalancePortfolio.date >= start_date)

            if end_date is not None:
                query = query.filter(ConsolidatedBalancePortfolio.date <= end_date)

            query = query.order_by(ConsolidatedBalancePortfolio.date.asc())

            cbps = query.all()
            return [to_model(cbp) for cbp in cbps]
        except SQLAlchemyError as e:
            return ConsolidatedBalancePortfolioError.DatabaseError

