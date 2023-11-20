from fastapi import HTTPException, status, APIRouter
from pydantic import BaseModel
from typing import List, Optional
from fastapi import Depends

from src.auth.user import User, get_current_user
from src.investment.domain.models import PortfolioModel
from src.investment.domain.portfolio_erros import PortfolioNotFound, PortfolioAlreadyExists
from src.investment.repository.db.db_connection import get_db_session
from src.investment.services.service_factory import ServiceFactory

router = APIRouter()


class NewPortfolioInput(BaseModel):
    name: str
    description: Optional[str]


@router.get("", response_model=List[PortfolioModel])
async def get_all_portfolios(
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    try:
        portfolio_service = ServiceFactory.create_portfolio_service(db_session)
        return portfolio_service.find_all(current_user.code)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{portfolio_code}", response_model=PortfolioModel)
async def get_portfolio(
        portfolio_code: str,
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    try:
        portfolio_service = ServiceFactory.create_portfolio_service(db_session)
        result = portfolio_service.find_by_code(current_user.code, portfolio_code)
        return result
    except PortfolioNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("", response_model=PortfolioModel)
async def create_portfolio(
        input: NewPortfolioInput,
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    try:
        portfolio_service = ServiceFactory.create_portfolio_service(db_session)
        portfolio_model = PortfolioModel(code=None, name=input.name, description=input.description,
                                         user_code=current_user.code)
        return portfolio_service.create(current_user.code, portfolio_model)
    except PortfolioAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))


@router.put("/{portfolio_code}", response_model=PortfolioModel)
async def update_portfolio(
        portfolio_code: str,
        portfolio_input: PortfolioModel,
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    portfolio_service = ServiceFactory.create_portfolio_service(db_session)
    try:
        return portfolio_service.update(current_user.code, portfolio_code, portfolio_input)
    except PortfolioNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{portfolio_code}")
async def delete_portfolio(
        portfolio_code: str,
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    try:
        portfolio_service = ServiceFactory.create_portfolio_service(db_session)
        portfolio_service.delete(current_user.code, portfolio_code)
        return {"message": "Portfolio deleted successfully"}
    except PortfolioNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
