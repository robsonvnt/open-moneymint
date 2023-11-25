import calendar
from datetime import date, datetime

from fastapi import APIRouter, Query, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Annotated
from fastapi import Depends

from auth.user import User, get_current_user
from finance.domain.account_erros import AccountNotFound
from finance.domain.financial_transaction_erros import FinancialTransactionNotFound
from finance.domain.models import TransactionType, FinancialTransactionModel
from finance.repository.db.db_connection import get_db_session
from finance.services.factory import ServiceFactory
from helpers import get_last_day_of_the_month

finance_transaction_router = APIRouter()
router = finance_transaction_router


class TransactionInput(BaseModel):
    account_code: str
    description: str
    category_code: str
    type: TransactionType
    date: date
    value: float


class TransactionResponse(BaseModel):
    code: str
    account_code: str
    description: str
    category_code: str
    type: TransactionType
    date: date
    value: float


@router.get("/transactions", response_model=List[TransactionResponse])
async def get_all_transactions(
        account_codes: Annotated[Optional[list[str]], Query()] = None,
        month: Optional[str] = Query(
            None, description="Start date in YYYY-MM format"
        ),
        start_date: Optional[date] = Query(
            None, description="Start date in YYYY-MM-DD format"
        ),
        end_date: Optional[date] = Query(
            None, description="End date in YYYY-MM-DD format"
        ),
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    try:
        transaction_serv = ServiceFactory.create_financial_transaction_service(db_session)
        account_serv = ServiceFactory.create_account_service(db_session)

        if not account_codes:
            account_codes = [account_code.code for account_code in account_serv.get_all_by_user_code(current_user.code)]

        # Validates whether transactions belongs to the logged in user
        for account_code in account_codes:
            account_serv.get_by_code(current_user.code, account_code)

        if month:
            month_date = datetime.strptime(month, "%Y-%m").date()
            start_date = month_date
            end_date = get_last_day_of_the_month(month_date)

        transactions = transaction_serv.filter_by_account_and_date(
            account_codes,
            start_date,
            end_date
        )
        return transactions
    except AccountNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/transactions/{transaction_code}", response_model=TransactionResponse)
async def get_transaction(
        transaction_code: str,
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    try:
        transaction_serv = ServiceFactory.create_financial_transaction_service(db_session)
        account_serv = ServiceFactory.create_account_service(db_session)
        transaction = transaction_serv.get_by_code(transaction_code)

        # Validates whether transaction belongs to the logged in user
        account_serv.get_by_code(current_user.code, transaction.account_code)
        return transaction
    except FinancialTransactionNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AccountNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/transactions", response_model=TransactionResponse)
async def create_transaction(
        new_transaction_data: TransactionInput,
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    try:
        transaction_serv = ServiceFactory.create_financial_transaction_service(db_session)
        new_transaction = transaction_serv.create(
            FinancialTransactionModel(**new_transaction_data.model_dump())
        )
        account_serv = ServiceFactory.create_account_service(db_session)

        # Validates whether transaction belongs to the logged in user
        account_serv.get_by_code(current_user.code, new_transaction.account_code)
        return new_transaction
    except FinancialTransactionNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AccountNotFound as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.put("/transactions/{transaction_code}", response_model=TransactionResponse)
async def update_transaction(
        transaction_code: str,
        new_transaction_data: TransactionInput,
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    try:
        transaction_serv = ServiceFactory.create_financial_transaction_service(db_session)

        # Validates whether transaction belongs to the logged in user
        db_transaction = transaction_serv.get_by_code(transaction_code)
        account_serv = ServiceFactory.create_account_service(db_session)
        account_serv.get_by_code(current_user.code, db_transaction.account_code)

        updated_transaction = transaction_serv.update(
            transaction_code, FinancialTransactionModel(**new_transaction_data.model_dump())
        )
        return updated_transaction
    except FinancialTransactionNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AccountNotFound as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.delete("/transactions/{transaction_code}")
async def update_transaction(
        transaction_code: str,
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    try:
        transaction_serv = ServiceFactory.create_financial_transaction_service(db_session)
        transaction = transaction_serv.get_by_code(transaction_code)

        # Validates whether transaction belongs to the logged in user
        account_serv = ServiceFactory.create_account_service(db_session)
        account_serv.get_by_code(current_user.code, transaction.account_code)

        transaction_serv.delete(transaction_code)
        return {"message": "Transaction deleted successfully"}
    except FinancialTransactionNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AccountNotFound as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
