from datetime import date, datetime
from typing import List, Optional, Annotated

from fastapi import APIRouter, Query, HTTPException, status
from fastapi import Depends
from pydantic import BaseModel

from auth.user import User, get_current_user
from finance.domain.account_erros import AccountConsolidationNotFound
from finance.domain.category_erros import CategoryNotFound
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
    category_code: Optional[str]
    type: TransactionType
    date: date
    value: float

    def __init__(self, **data):
        data.setdefault('category_code', None)
        super().__init__(**data)


class TransactionResponse(BaseModel):
    code: str
    account_code: str
    description: str
    category_code: Optional[str]
    type: TransactionType
    date: date
    value: float


@router.get("/transactions", response_model=List[TransactionResponse])
async def get_all_transactions(
        account_codes: Annotated[Optional[list[str]], Query()] = None,
        category_codes: Annotated[Optional[list[str]], Query()] = None,
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
        category_service = ServiceFactory.create_category_service(db_session)

        if not account_codes:
            account_codes = [account_code.code for account_code in account_serv.get_all_by_user_code(current_user.code)]

        # TODO Move to Service
        # Validates whether accounts belongs to the logged in user
        for account_code in account_codes:
            account_serv.get_by_code(current_user.code, account_code)

        # TODO Move to Service
        # Validates whether categories belongs to the logged in user
        category_codes_filter = []
        if category_codes:
            for category_code in category_codes:
                category = category_service.get_by_code(category_code)
                if category.user_code != current_user.code:
                    raise CategoryNotFound()
                else:
                    children = category_service.list_all_children(category.code, category.user_code)
                    category_codes_filter.append(category.code)
                    category_codes_filter.extend([cat.code for cat in children])

        if month:
            month_date = datetime.strptime(month, "%Y-%m").date()
            start_date = month_date
            end_date = get_last_day_of_the_month(month_date)

        transactions = transaction_serv.filter_by_account_and_date(
            account_codes,
            category_codes_filter,
            start_date,
            end_date
        )
        return transactions
    except AccountConsolidationNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except CategoryNotFound as e:
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
    except AccountConsolidationNotFound as e:
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
            current_user.code,
            FinancialTransactionModel(**new_transaction_data.model_dump())
        )
        account_serv = ServiceFactory.create_account_service(db_session)

        # Validates whether transaction belongs to the logged in user
        account_serv.get_by_code(current_user.code, new_transaction.account_code)
        return new_transaction
    except FinancialTransactionNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AccountConsolidationNotFound as e:
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
            current_user.code,
            transaction_code, FinancialTransactionModel(**new_transaction_data.model_dump())
        )
        return updated_transaction
    except FinancialTransactionNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AccountConsolidationNotFound as e:
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

        transaction_serv.delete(current_user.code, transaction_code)
        return {"message": "Transaction deleted successfully"}
    except FinancialTransactionNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AccountConsolidationNotFound as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
