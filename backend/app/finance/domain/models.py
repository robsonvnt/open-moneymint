from enum import Enum
from typing import Optional
from datetime import date

from pydantic import BaseModel


class AccountModel(BaseModel):
    code: Optional[str]
    name: str
    description: Optional[str]
    user_code: str
    created_at: Optional[date]

    def __init__(self, **data):
        data.setdefault('code', None)
        data.setdefault('created_at', None)
        data.setdefault('description', None)
        super().__init__(**data)


class TransactionType(Enum):
    TRANSFER = "TRANSFER"
    WITHDRAWAL = "WITHDRAWAL"
    DEPOSIT = "DEPOSIT"


class CategoryModel(BaseModel):
    code: Optional[str]
    name: str
    parent_category_code: Optional[str]
    user_code: str
    created_at: Optional[date]

    def __init__(self, **data):
        data.setdefault('code', None)
        data.setdefault('created_at', None)
        super().__init__(**data)


class TransactionModel(BaseModel):
    code: Optional[str]
    account_code: str
    description: float
    category_code: str
    type: TransactionType
    date: date
    value: float


class ConsolidatedAccountModel(BaseModel):
    account_code: Optional[str]
    date: date
    balance: float
