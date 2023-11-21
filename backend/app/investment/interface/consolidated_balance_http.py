from fastapi import APIRouter, status, Query, HTTPException, Depends
from typing import Optional
from datetime import date

from auth.user import User, get_current_user
from investment.domain.models import ConsolidatedPortfolioModel
from investment.repository.db.db_connection import get_db_session
from investment.services.consolidated_service import ConsolidatedPortfolioService
from investment.services.service_factory import ServiceFactory

router = APIRouter()


@router.get("/{portfolio_code}/consolidations")
async def get_consolidated_balance(
        portfolio_code: str,
        start_date: Optional[date] = Query(None, description="Start date in YYYY-MM-DD format"),
        end_date: Optional[date] = Query(None, description="End date in YYYY-MM-DD format"),
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    consolidated_balance_service: ConsolidatedPortfolioService = ServiceFactory.create_consolidated_balance_service(db_session)
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
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    try:
        consolidated_balance_service = ServiceFactory.create_consolidated_balance_service(db_session)
        return consolidated_balance_service.consolidate_portfolio(current_user.code, portfolio_code)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
