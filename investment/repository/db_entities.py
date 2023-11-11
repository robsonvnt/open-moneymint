from sqlalchemy import create_engine, Column, Integer, String, Float, Date, and_, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_mixins import AllFeaturesMixin

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