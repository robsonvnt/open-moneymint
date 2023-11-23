from sqlalchemy import Column, Float, Date, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_mixins import AllFeaturesMixin

Base = declarative_base()


# Modelo de Investment
class Account(Base, AllFeaturesMixin):

    def __init__(self, **kwargs):
        kwargs.setdefault('id', None)
        super().__init__(**kwargs)

    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True, unique=True)
    name = Column(String, index=True)
    description = Column(String)
    user_code = Column(String, index=True)
    created_at = Column(Date)


class Category(Base, AllFeaturesMixin):

    def __init__(self, **kwargs):
        kwargs.setdefault('id', None)
        super().__init__(**kwargs)

    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    code = Column(String, index=True, unique=True)
    name = Column(String, index=True)
    user_code = Column(String, index=True)
    parent_category_code = Column(String, index=True)
    created_at = Column(Date)


