from fastapi import HTTPException, status, APIRouter
from pydantic import BaseModel
from typing import List, Optional
from fastapi import Depends

from auth.user import User, get_current_user
from finance.domain.models import CategoryModel
from finance.repository.db.db_connection import get_db_session
from finance.services.factory import ServiceFactory

account_router = APIRouter()


class NewCategoryInput(BaseModel):
    name: str
    parent_category_code: Optional[str]


@account_router.get("/categories", response_model=List[CategoryModel])
async def get_all_accounts(
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    account_service = ServiceFactory.create_account_service(db_session)
    return account_service.get_all_by_user_code(current_user.code)
#
#
# @account_router.get("/accounts/{account_code}", response_model=AccountModel)
# async def get_account(
#         account_code: str,
#         db_session=Depends(get_db_session),
#         current_user: User = Depends(get_current_user)
# ):
#     try:
#         account_service = ServiceFactory.create_account_service(db_session)
#         result = account_service.get_by_code(current_user.code, account_code)
#         return result
#     except AccountNotFound as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
#
#
# @account_router.post("/accounts", response_model=AccountModel)
# async def create_account(
#         input: NewAccountInput,
#         db_session=Depends(get_db_session),
#         current_user: User = Depends(get_current_user)
# ):
#     account_service = ServiceFactory.create_account_service(db_session)
#     account_model = AccountModel(name=input.name, description=input.description, user_code=current_user.code)
#     return account_service.create(account_model)
#
#
# @account_router.put("/accounts/{account_code}", response_model=AccountModel)
# async def update_account(
#         account_code: str,
#         account_input: AccountModel,
#         db_session=Depends(get_db_session),
#         current_user: User = Depends(get_current_user)
# ):
#     account_service = ServiceFactory.create_account_service(db_session)
#     try:
#         return account_service.update(current_user.code, account_code, account_input)
#     except AccountNotFound as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
#
#
# @account_router.delete("/accounts/{account_code}")
# async def delete_account(
#         account_code: str,
#         db_session=Depends(get_db_session),
#         current_user: User = Depends(get_current_user)
# ):
#     try:
#         account_service = ServiceFactory.create_account_service(db_session)
#         account_service.delete(current_user.code, account_code)
#         return {"message": "Account deleted successfully"}
#     except AccountNotFound as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))