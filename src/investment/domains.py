from enum import Enum
from typing import Optional
from datetime import date

from pydantic import BaseModel
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class PortfolioModel(BaseModel):
    code: Optional[str]
    name: str
    description: Optional[str]


class PortfolioConsolidationModel(BaseModel):
    portfolio_code: str
    date: date
    balance: float
    amount_invested: float


class PortfolioOverviewModel(BaseModel):
    code: str
    name: str
    description: str
    amount_invested: float
    current_balance: float
    portfolio_yield: float
    portfolio_gross_nominal_yield: float


class PortfolioError(Enum):
    AlreadyExists = "Portfolio already exists"
    PortfolioNotFound = "Portfolio not found"
    DatabaseError = "Database error"
    Unexpected = "Unexpected error"
    OperationNotPermitted = "Operation not permitted"


class InvestmentError(Enum):
    AlreadyExists = "Investment already exists"
    InvestmentNotFound = "Investment not found"
    ColumnDoesNotExist = "Column does not exist"
    DatabaseError = "Database error"
    Unexpected = "Unexpected error"
    NoAssetsFound = "No Assets Found error"
    OperationNotPermitted = "Operation not permitted"


class AssetType(str, Enum):
    STOCK = "STOCK"
    REIT = "REIT"
    FIXED_INCOME = "FIXED_INCOME"


class TransactionError(Enum):
    TransactionNotFound = "Transaction not found"
    DatabaseError = "Database error"
    Unexpected = "Unexpected error"
    OperationNotPermitted = "Operation not permitted"


class InvestmentModel(BaseModel):
    code: Optional[str]
    portfolio_code: str
    asset_type: AssetType
    ticker: str
    quantity: float
    purchase_price: float
    current_average_price: Optional[float]
    purchase_date: date


class TransactionType(Enum):
    BUY = "BUY"
    SELL = "SELL"
    INTEREST = "INTEREST"
    WITHDRAWAL = "WITHDRAWAL"
    DEPOSIT = "DEPOSIT"


class TransactionModel(BaseModel):
    code: Optional[str]
    investment_code: str
    type: TransactionType
    date: date
    quantity: int
    price: float


class ConsolidatedPortfolioError(Enum):
    DatabaseError = "Database error"
    ConsolidatedPortfolioNotFound = "ConsolidatedPortfolio Not Found."
    Unexpected = "Unexpected error"


class ConsolidatedPortfolioModel(BaseModel):
    portfolio_code: Optional[str]
    date: date
    balance: float
    amount_invested: float
