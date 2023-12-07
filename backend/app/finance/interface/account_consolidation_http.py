from datetime import datetime, date, timedelta
from typing import List, Annotated, Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi.params import Query
from pydantic import BaseModel

from auth.user import User, get_current_user
from finance.domain.models import AccountConsolidationModel
from finance.repository.db.db_connection import get_db_session
from finance.services.factory import ServiceFactory
from helpers import get_last_day_of_the_month

account_consolidation_router = APIRouter()


class CategoryValueResponse(BaseModel):
    category: str
    value: float


@account_consolidation_router.get("/consolidations", response_model=List[AccountConsolidationModel])
async def get_all_consolidations(
        db_session=Depends(get_db_session),
        account_codes: Annotated[Optional[list[str]], Query()] = None,
        month: Optional[str] = Query(
            None, description="Start month in YYYY-MM format"
        ),
        start_month: Optional[str] = Query(
            None, description="Start month in YYYY-MM format"
        ),
        end_month: Optional[str] = Query(
            None, description="End month in YYYY-MM format"
        ),
        current_user: User = Depends(get_current_user)
):
    start_month_date = None
    end_month_date = None

    if month:
        start_month_date = datetime.strptime(month, "%Y-%m").date().replace(day=1)
        end_month_date = get_last_day_of_the_month(start_month_date)
    if start_month:
        start_month_date = datetime.strptime(start_month, "%Y-%m").date().replace(day=1)
    if end_month:
        end_month_date = datetime.strptime(end_month, "%Y-%m").date().replace(day=1)

    account_consolidations_service = ServiceFactory.create_account_consolidations_service(db_session)
    return account_consolidations_service.find_all_by_account(account_codes, start_month_date, end_month_date)


@account_consolidation_router.get("/consolidations/last-month", response_model=List[AccountConsolidationModel])
async def get_last_month_consolidations(
        db_session=Depends(get_db_session),
        account_codes: Annotated[Optional[list[str]], Query()] = None,
        current_user: User = Depends(get_current_user)
):
    preview_month = (date.today().replace(day=1) - timedelta(days=1)).replace(day=1)

    account_consolidations_service = ServiceFactory.create_account_consolidations_service(db_session)
    return account_consolidations_service.find_by_account_month(account_codes, preview_month)


@account_consolidation_router.get("/consolidations/current-month", response_model=List[AccountConsolidationModel])
async def get_current_month_consolidations(
        db_session=Depends(get_db_session),
        account_codes: Annotated[Optional[list[str]], Query()] = None,
        current_user: User = Depends(get_current_user)
):
    current_month = date.today().replace(day=1)

    account_consolidations_service = ServiceFactory.create_account_consolidations_service(db_session)
    return account_consolidations_service.find_by_account_month(account_codes, current_month)


@account_consolidation_router.get("/consolidations/grouped-by-category")
async def get_sum_consolidations_grouped_by_category(
        db_session=Depends(get_db_session),
        account_codes: Annotated[Optional[list[str]], Query()] = None,
        month: Optional[str] = Query(
            None, description="Start month in YYYY-MM format"
        ),
        start_month: Optional[str] = Query(
            None, description="Start month in YYYY-MM format"
        ),
        end_month: Optional[str] = Query(
            None, description="End month in YYYY-MM format"
        ),
        current_user: User = Depends(get_current_user)
):
    start_month_date = None
    end_month_date = None

    if month:
        start_month_date = datetime.strptime(month, "%Y-%m").date().replace(day=1)
        end_month_date = get_last_day_of_the_month(start_month_date)
    if start_month:
        start_month_date = datetime.strptime(start_month, "%Y-%m").date().replace(day=1)
    if end_month:
        end_month_date = datetime.strptime(end_month, "%Y-%m").date().replace(day=1)

    account_consolidations_service = ServiceFactory.create_account_consolidations_service(db_session)
    return account_consolidations_service.get_sum_consolidations_grouped_by_category(
        current_user.code, account_codes, start_month_date, end_month_date
    )
