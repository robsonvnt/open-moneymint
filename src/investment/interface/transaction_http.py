from datetime import date

from fastapi import HTTPException, status, APIRouter
from pydantic import BaseModel
from typing import List
from fastapi import Depends

from src.auth.user import get_current_user, User
from src.investment.domain.investment_errors import InvestmentNotFound
from src.investment.domain.models import TransactionType, TransactionModel
from src.investment.domain.portfolio_erros import PortfolioNotFound
from src.investment.domain.transaction_errors import TransactionNotFound, TransactionOperationNotPermitted
from src.investment.repository.db.db_connection import get_db_session
from src.investment.services.service_factory import ServiceFactory

router = APIRouter()


class NewTransactionInput(BaseModel):
    investment_code: str
    type: TransactionType
    date: date
    quantity: int
    price: float


@router.get("/{portfolio_code}/investments/{investment_code}/transactions",
            response_model=List[TransactionModel])
async def get_all_transactions(
        portfolio_code,
        investment_code,
        db_session=Depends(get_db_session),
        current_user=Depends(get_current_user)
):
    try:
        transactions_service = ServiceFactory.create_transaction_service(db_session)
        return transactions_service.find_all(portfolio_code, investment_code)
    except (InvestmentNotFound, PortfolioNotFound) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{portfolio_code}/investments/{investment_code}/transactions/{transaction_code}",
            response_model=TransactionModel)
async def get_transaction(
        portfolio_code,
        investment_code,
        transaction_code,
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    try:
        transactions_service = ServiceFactory.create_transaction_service(db_session)
        return transactions_service.find_by_code(current_user.code, portfolio_code, investment_code, transaction_code)
    except (InvestmentNotFound, PortfolioNotFound, TransactionNotFound) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{portfolio_code}/investments/{investment_code}/transactions", response_model=TransactionModel)
async def create_transaction(
        portfolio_code,
        investment_code,
        input_new_transaction: NewTransactionInput,
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    try:
        transactions_service = ServiceFactory.create_transaction_service(db_session)
        transaction_model = TransactionModel(code=None, **input_new_transaction.model_dump())
        return transactions_service.create(current_user.code, portfolio_code, investment_code, transaction_model)
    except TransactionOperationNotPermitted as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=str(e))
    except (InvestmentNotFound, PortfolioNotFound) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{portfolio_code}/investments/{investment_code}/transactions/{transaction_code}")
async def delete_transaction(
        portfolio_code,
        investment_code,
        transaction_code,
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    try:
        transactions_service = ServiceFactory.create_transaction_service(db_session)
        transaction_model = transactions_service.find_by_code(current_user.code, portfolio_code, investment_code, transaction_code)
        transactions_service.delete(current_user.code, portfolio_code, investment_code, transaction_model)
        return {"message": "Transaction deleted successfully"}
    except TransactionOperationNotPermitted as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=str(e))
    except (InvestmentNotFound, PortfolioNotFound, TransactionNotFound) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
