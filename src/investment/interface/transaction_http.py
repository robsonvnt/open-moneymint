from datetime import date

from fastapi import HTTPException, status, APIRouter
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import JSONResponse
from fastapi import Depends

from src.investment.domain.investment_errors import InvestmentNotFound
from src.investment.domain.models import PortfolioModel, TransactionType, TransactionModel
from src.investment.domain.portfolio_erros import PortfolioNotFound, PortfolioAlreadyExists
from src.investment.domain.transaction_errors import TransactionNotFound, TransactionOperationNotPermitted
from src.investment.repository.db.db_connection import get_db_session
from src.investment.repository.db.db_entities import Investment
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
        db_session=Depends(get_db_session)
):
    try:
        transactions_service = ServiceFactory.create_transaction_service(db_session)
        return transactions_service.find_all(portfolio_code, investment_code)
    except (InvestmentNotFound, PortfolioNotFound) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{portfolio_code}/investments/{investment_code}/transactions/{transaction_code}",
            response_model=TransactionModel)
async def get_transaction(
        portfolio_code,
        investment_code,
        transaction_code,
        db_session=Depends(get_db_session)
):
    try:
        transactions_service = ServiceFactory.create_transaction_service(db_session)
        return transactions_service.find_by_code(portfolio_code, investment_code, transaction_code)
    except (InvestmentNotFound, PortfolioNotFound, TransactionNotFound) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/{portfolio_code}/investments/{investment_code}/transactions", response_model=TransactionModel)
async def create_transaction(
        portfolio_code,
        investment_code,
        input: NewTransactionInput,
        db_session=Depends(get_db_session)
):
    try:
        transactions_service = ServiceFactory.create_transaction_service(db_session)
        transaction_model = TransactionModel(code=None, **input.model_dump())
        return transactions_service.create(portfolio_code, investment_code, transaction_model)
    except TransactionOperationNotPermitted as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=str(e))
    except (InvestmentNotFound, PortfolioNotFound) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))
#
#
# @router.put("/{portfolio_code}", response_model=PortfolioModel)
# async def update_portfolio(
#         portfolio_code: str,
#         input: PortfolioModel,
#         db_session=Depends(get_db_session)
# ):
#     portfolio_service = ServiceFactory.create_portfolio_service(db_session)
#     try:
#         return portfolio_service.update_portfolio(portfolio_code, input)
#     except PortfolioNotFound as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
#
#
# @router.delete("/{portfolio_code}")
# async def delete_portfolio(
#         portfolio_code: str,
#         db_session=Depends(get_db_session)
# ):
#     try:
#         portfolio_service = ServiceFactory.create_portfolio_service(db_session)
#         portfolio_service.delete_portfolio(portfolio_code)
#         return {"message": "Portfolio deleted successfully"}
#     except PortfolioNotFound as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
