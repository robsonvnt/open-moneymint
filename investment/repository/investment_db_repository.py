from sqlalchemy import create_engine, Column, Integer, String, Float, Date, and_, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy_mixins import AllFeaturesMixin

# Configuração do banco de dados
from investment.domains import InvestmentError, InvestmentModel
from investment.helpers import generate_code

Base = declarative_base()


# Modelo de Investment
class Investment(Base, AllFeaturesMixin):
    __tablename__ = 'investments'
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True)
    portfolio_code = Column(String, index=True)
    asset_type = Column(String)
    ticker = Column(String)
    quantity = Column(Float)
    purchase_price = Column(Float)
    current_average_price = Column(Float)
    purchase_date = Column(Date)


def to_database(investment_model: InvestmentModel) -> Investment:
    return Investment(**investment_model.model_dump())


def to_model(investment: Investment) -> InvestmentModel:
    return InvestmentModel(**investment.to_dict())


# Repositório de Investment
class InvestmentRepo:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create(self, new_investment_data):
        session = self.Session()
        code = generate_code()
        new_investment = Investment(id=None, **new_investment_data.dict())
        new_investment.code = code
        try:
            session.add(new_investment)
            session.commit()
            session.refresh(new_investment)
            return to_model(new_investment)
        except Exception as e:
            if 'unique constraint' in str(e).lower():
                return InvestmentError.AlreadyExists
            else:
                return InvestmentError.DatabaseError
        finally:
            session.close()

    def find_by_code(self, portfolio_code: str, investment_code):
        session = self.Session()
        investment = session.query(Investment).filter(
            Investment.code == investment_code,
            Investment.portfolio_code == portfolio_code,
        ).first()
        if investment is None:
            return InvestmentError.InvestmentNotFound
        return to_model(investment)

    def find_all_by_portfolio_code(self, portfolio_code: str):
        session = self.Session()
        investments = session.query(Investment).filter(
            Investment.portfolio_code == portfolio_code,
        ).all()
        return [to_model(inv) for inv in investments]

    def delete(self, portfolio_code: str, investment_code: str):
        try:
            session = self.Session()
            investment = session.query(Investment).filter(
                Investment.portfolio_code == portfolio_code,
                Investment.code == investment_code
            ).first()
            if investment is None:
                return InvestmentError.InvestmentNotFound
            session.delete(investment)
            session.commit()
            return True
        except Exception as e:
            return InvestmentError.DatabaseError

    def update(self, portfolio_code: str, investment_code, updated_investment_data: InvestmentModel):
        session = self.Session()
        investment = session.query(Investment).filter(
            Investment.portfolio_code == portfolio_code,
            Investment.code == investment_code
        ).first()
        if investment is None:
            return InvestmentError.InvestmentNotFound
        tmp = updated_investment_data.model_dump()
        for key, value in updated_investment_data.model_dump().items():
            setattr(investment, key, value)
        session.commit()
        session.refresh(investment)
        return to_model(investment)

    def get_diversification_portfolio(self, portfolio_code):
        session = self.Session()
        try:
            query = text(
                "SELECT asset_type, SUM(quantity * current_average_price) AS total_weight "
                "FROM investments WHERE portfolio_code = :portfolio_code GROUP BY asset_type"
            )
            result = session.execute(query, {"portfolio_code": portfolio_code}).fetchall()
            if not result:
                return InvestmentError.NoAssetsFound
            diversification_portfolio = {row[0]: row[1] for row in result}
            return diversification_portfolio
        except Exception as e:
            return InvestmentError.DatabaseError
