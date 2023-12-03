from sqlalchemy import Column, Float, Date, Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_mixins import AllFeaturesMixin

from finance.domain.models import TransactionType

Base = declarative_base()


# Modelo de Investment
class Account(Base, AllFeaturesMixin):
    __tablename__ = 'finances_accounts'
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True, unique=True)
    name = Column(String, index=True)
    description = Column(String)
    user_code = Column(String, index=True)
    balance = Column(Float, default=0)
    created_at = Column(Date)

    def __init__(self, **kwargs):
        kwargs.setdefault('id', None)
        super().__init__(**kwargs)


class Category(Base, AllFeaturesMixin):
    __tablename__ = 'finances_categories'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    code = Column(String, index=True, unique=True)
    name = Column(String, index=True)
    user_code = Column(String, index=True)
    parent_category_code = Column(String, index=True)
    created_at = Column(Date)

    def __init__(self, **kwargs):
        kwargs.setdefault('id', None)
        super().__init__(**kwargs)


class FinancialTransaction(Base, AllFeaturesMixin):
    __tablename__ = 'finances_transactions'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    code = Column(String, index=True, unique=True)
    account_code = Column(String, index=True)
    description = Column(String)
    category_code = Column(String, index=True, nullable=True)
    type = Column(String)
    date = Column(Date)
    value = Column(Float)

    def __init__(self, **kwargs):
        kwargs.setdefault('id', None)
        if isinstance(kwargs.get('type'), TransactionType):
            kwargs['type'] = kwargs['type'].value
        super().__init__(**kwargs)


class AccountConsolidation(Base, AllFeaturesMixin):
    __tablename__ = 'finances_account_consolidations'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    account_code = Column(String, ForeignKey('finances_accounts.code'), index=True)
    month = Column(Date)
    balance = Column(Float)

    __table_args__ = (
        UniqueConstraint('account_code', 'month', name='finances_consolidated_account_account_month_uc'),
    )

    def __init__(self, **kwargs):
        kwargs.setdefault('id', None)
        super().__init__(**kwargs)
