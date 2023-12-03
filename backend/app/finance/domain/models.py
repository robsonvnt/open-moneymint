from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class AccountModel(BaseModel):
    code: Optional[str]
    name: str
    description: Optional[str]
    user_code: str
    balance: float
    created_at: Optional[date]

    def __init__(self, **data):
        data.setdefault('code', None)
        data.setdefault('created_at', None)
        data.setdefault('description', None)
        data.setdefault('balance', 0)
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
        if data["parent_category_code"] == "":
            data["parent_category_code"] = None
        data.setdefault('parent_category_code', None)
        super().__init__(**data)


class FinancialTransactionModel(BaseModel):
    code: Optional[str]
    account_code: str
    description: str
    category_code: Optional[str]
    type: TransactionType
    date: date
    value: float

    def __init__(self, **data):
        data.setdefault('code', None)
        if isinstance(data.get('type'), str):
            data['type'] = TransactionType[data['type']]
        super().__init__(**data)


class AccountConsolidationModel(BaseModel):
    account_code: Optional[str]
    month: date
    balance: float
