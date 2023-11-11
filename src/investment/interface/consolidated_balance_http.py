from fastapi import APIRouter, status, Query, HTTPException
from typing import Optional
from datetime import date

from src.investment.domains import ConsolidatedPortfolioModel
from src.investment.services.consolidated_service import ConsolidatedPortfolioService
from src.investment.services.service_factory import ServiceFactory

router = APIRouter()

consolidated_balance_service: ConsolidatedPortfolioService = ServiceFactory.create_consolidated_balance_service()


@router.get("/{portfolio_code}/consolidations")
async def get_consolidated_balance(
        portfolio_code: str,
        start_date: Optional[date] = Query(None, description="Start date in YYYY-MM-DD format"),
        end_date: Optional[date] = Query(None, description="End date in YYYY-MM-DD format"),
):
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
        portfolio_code: str
):
    result = consolidated_balance_service.consolidate_portfolio(portfolio_code)
    match result:
        case ConsolidatedPortfolioModel():
            return result
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred."
            )
