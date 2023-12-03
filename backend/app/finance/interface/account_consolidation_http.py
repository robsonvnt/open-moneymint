from datetime import datetime
from typing import List, Annotated, Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi.params import Query

from auth.user import User, get_current_user
from finance.domain.models import AccountConsolidationModel
from finance.repository.db.db_connection import get_db_session
from finance.services.factory import ServiceFactory

account_consolidation_router = APIRouter()


@account_consolidation_router.get("/consolidations", response_model=List[AccountConsolidationModel])
async def get_all_consolidations(
        db_session=Depends(get_db_session),
        account_code: str = Query(),
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
    if start_month:
        start_month_date = datetime.strptime(start_month, "%Y-%m").date().replace(day=1)
    if end_month:
        end_month_date = datetime.strptime(end_month, "%Y-%m").date().replace(day=1)

    account_consolidations_service = ServiceFactory.create_account_consolidations_service(db_session)
    return account_consolidations_service.find_all_by_account(account_code, start_month_date, end_month_date)
