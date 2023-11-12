from fastapi import HTTPException, status, APIRouter
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import JSONResponse
from fastapi import Depends

from src.investment.domains import PortfolioModel, PortfolioError
from src.investment.repository.db_connection import get_db_session
from src.investment.services.service_factory import ServiceFactory

router = APIRouter()


class NewPortfolioInput(BaseModel):
    name: str
    description: Optional[str]


@router.get("", response_model=List[PortfolioModel])
async def get_all_portfolios(
        db_session=Depends(get_db_session)
):
    portfolio_service = ServiceFactory.create_portfolio_service(db_session)
    result = portfolio_service.find_all_portfolios()
    match result:
        case list():
            return result
        case PortfolioError:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": result.value}
            )


@router.get("/{portfolio_code}", response_model=PortfolioModel)
async def get_portfolio(
        portfolio_code: str,
        db_session=Depends(get_db_session)
):
    portfolio_service = ServiceFactory.create_portfolio_service(db_session)
    result = portfolio_service.find_portfolio_by_code(portfolio_code)

    match result:
        case PortfolioModel():
            return result
        case PortfolioError.PortfolioNotFound:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": result.value}
            )
        case _:
            JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": result.value}
            )


@router.post("", response_model=PortfolioModel)
async def create_portfolio(
        input: NewPortfolioInput,
        db_session=Depends(get_db_session)
):
    portfolio_service = ServiceFactory.create_portfolio_service(db_session)
    try:
        portfolio_model = PortfolioModel(code=None, name=input.name, description=input.description)
        result = portfolio_service.create_portfolio(portfolio_model)
    except Exception as e:
        JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(e)}
        )

    match result:
        case PortfolioModel():
            return result
        case PortfolioError.AlreadyExists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=result.value)


@router.put("/{portfolio_code}", response_model=PortfolioModel)
async def update_portfolio(
        portfolio_code: str,
        input: PortfolioModel,
        db_session=Depends(get_db_session)
):
    portfolio_service = ServiceFactory.create_portfolio_service(db_session)
    try:
        result = portfolio_service.update_portfolio(portfolio_code, input)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    match result:
        case PortfolioModel():
            return result
        case PortfolioError.PortfolioNotFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=result.value)


@router.delete("/{portfolio_code}")
async def delete_portfolio(
        portfolio_code: str,
        db_session=Depends(get_db_session)
):
    portfolio_service = ServiceFactory.create_portfolio_service(db_session)
    try:
        result = portfolio_service.delete_portfolio(portfolio_code)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(e)}
        )

    match result:
        case None:
            return {"message": "Portfolio deleted successfully"}
        case PortfolioError.PortfolioNotFound:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": result.value}
            )
        case _:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "An unexpected error occurred"}
            )
