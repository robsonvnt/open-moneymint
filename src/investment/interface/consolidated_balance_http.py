from fastapi import APIRouter, status, Query, HTTPException, Depends
from typing import Optional
from datetime import date

from src.investment.domains import ConsolidatedPortfolioModel
from src.investment.repository.db.db_connection import get_db_session
from src.investment.services.service_factory import ServiceFactory

router = APIRouter()


@router.get("/{portfolio_code}/consolidations")
async def get_consolidated_balance(
        portfolio_code: str,
        start_date: Optional[date] = Query(None, description="Start date in YYYY-MM-DD format"),
        end_date: Optional[date] = Query(None, description="End date in YYYY-MM-DD format"),
        db_session=Depends(get_db_session)
):
    consolidated_balance_service = ServiceFactory.create_consolidated_balance_service(db_session)
    result = consolidated_balance_service.filter_by_date_range(portfolio_code, start_date, end_date)

    match result:
        case list():
            return result
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred."
            )


@router.post("/{portfolio_code}/consolidations/consolidate")
async def consolidate_balance(
        portfolio_code: str,
        db_session=Depends(get_db_session)
):
    consolidated_balance_service = ServiceFactory.create_consolidated_balance_service(db_session)
    result = consolidated_balance_service.consolidate_portfolio(portfolio_code)
    match result:
        case ConsolidatedPortfolioModel():
            return result
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred."
            )
