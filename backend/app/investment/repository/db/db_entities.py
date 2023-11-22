from sqlalchemy import Column, Float, Date, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_mixins import AllFeaturesMixin

Base = declarative_base()


# Modelo de Investment
class Investment(Base, AllFeaturesMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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


class ConsolidatedPortfolio(Base, AllFeaturesMixin):
    __tablename__ = 'consolidated_balance_portfolios'
    id = Column(Integer, primary_key=True)
    portfolio_code = Column(String)
    date = Column(Date)
    balance = Column(Float)
    amount_invested = Column(Float)


class Portfolio(Base, AllFeaturesMixin):
    __tablename__ = 'portfolios'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    user_code = Column(Text)


class Transaction(Base, AllFeaturesMixin):
    __tablename__ = 'transactions'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    code = Column(String(10), index=True)
    investment_code = Column(String(10), index=True)
    type = Column(String)
    date = Column(Date, index=True)
    quantity = Column(Integer)
    price = Column(Float)
