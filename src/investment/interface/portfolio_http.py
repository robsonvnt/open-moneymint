from fastapi import HTTPException, status, APIRouter
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import JSONResponse
from fastapi import Depends

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
        db_session=Depends(get_db_session)
):
    try:
        portfolio_service = ServiceFactory.create_portfolio_service(db_session)
        return portfolio_service.find_all_portfolios()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{portfolio_code}", response_model=PortfolioModel)
async def get_portfolio(
        portfolio_code: str,
        db_session=Depends(get_db_session)
):
    try:
        portfolio_service = ServiceFactory.create_portfolio_service(db_session)
        result = portfolio_service.find_portfolio_by_code(portfolio_code)
        return result
    except PortfolioNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("", response_model=PortfolioModel)
async def create_portfolio(
        input: NewPortfolioInput,
        db_session=Depends(get_db_session)
):
    try:
        portfolio_service = ServiceFactory.create_portfolio_service(db_session)
        portfolio_model = PortfolioModel(code=None, name=input.name, description=input.description)
        return portfolio_service.create_portfolio(portfolio_model)
    except PortfolioAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))


@router.put("/{portfolio_code}", response_model=PortfolioModel)
async def update_portfolio(
        portfolio_code: str,
        input: PortfolioModel,
        db_session=Depends(get_db_session)
):
    portfolio_service = ServiceFactory.create_portfolio_service(db_session)
    try:
        return portfolio_service.update_portfolio(portfolio_code, input)
    except PortfolioNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{portfolio_code}")
async def delete_portfolio(
        portfolio_code: str,
        db_session=Depends(get_db_session)
):
    try:
        portfolio_service = ServiceFactory.create_portfolio_service(db_session)
        portfolio_service.delete_portfolio(portfolio_code)
        return {"message": "Portfolio deleted successfully"}
    except PortfolioNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
