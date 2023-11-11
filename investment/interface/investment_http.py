from http.client import HTTPResponse

from fastapi import HTTPException, status, APIRouter
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

import constants
from constants import SUCCESS_RESULT
from investment.domains import InvestmentModel, PortfolioError, InvestmentError, PortfolioConsolidationModel, \
    PortfolioOverviewModel
from investment.services.investment_service import InvestmentService
from investment.services.service_factory import ServiceFactory

router = APIRouter()

investment_service: InvestmentService = ServiceFactory.create_investment_service()


class NewInvestmentInput(BaseModel):
    portfolio_code: str
    asset_type: str
    ticker: str
    quantity: float
    purchase_price: float
    current_average_price: Optional[float]
    purchase_date: date


class AssetTypeValue(BaseModel):
    asset_type: str
    value: float


@router.post("/{portfolio_code}/investments", response_model=InvestmentModel)
async def create_investment(portfolio_code, input: NewInvestmentInput):
    if not portfolio_code == input.portfolio_code:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Portfolio code does not match.")

    investment_model = InvestmentModel(code=None, **input.model_dump())
    result = investment_service.create_investment(investment_model)

    match result:
        case InvestmentModel():
            return result
        case PortfolioError.PortfolioNotFound:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=result.value)
        case _:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Failed to retrieve investments.")


@router.get("/{portfolio_code}/investments/{investment_code}", response_model=InvestmentModel)
async def get_investment(portfolio_code: str, investment_code: str):
    result = investment_service.find_investment_by_code(portfolio_code, investment_code)

    match result:
        case InvestmentModel():
            return result
        case InvestmentError.InvestmentNotFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=result.value)
        case _:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{portfolio_code}/investments", response_model=List[InvestmentModel])
async def get_all_investments(portfolio_code: str, order_by: str = None):
    """
    Recupera todos os investimentos associados a um determinado código de portfólio.

    Este endpoint permite a recuperação de uma lista de investimentos filtrada pelo código do portfólio.
    Os investimentos podem ser ordenados com base em qualquer coluna disponível, de forma ascendente ou descendente.

    Parâmetros:
    - portfolio_code (str): O código do portfólio para o qual os investimentos são buscados.
    - order_by (str, opcional): Parâmetro de ordenação para os resultados.
      Deve ser o nome da coluna pelo qual ordenar. Para ordenação ascendente, forneça apenas o nome da coluna.
      Para ordenação descendente, adicione ".desc" após o nome da coluna (por exemplo, "purchase_date.desc").

    Retornos:
    - Lista de InvestmentModel: Uma lista de modelos de investimento correspondentes ao código do portfólio fornecido.
    - HTTP 404 Not Found: Erro levantado se o portfólio especificado não for encontrado.
    - HTTP 400 Bad Request: Erro levantado se o parâmetro 'order_by' especificar uma coluna que não existe.
    - HTTP 500 Internal Server Error: Erro levantado para qualquer outra falha no servidor.

    Exceções são tratadas para identificar portfólios não encontrados, colunas de ordenação inválidas e erros gerais de servidor,
    proporcionando uma resposta apropriada ao cliente.
    """
    result = investment_service.find_all_investments(portfolio_code, order_by)
    match result:
        case list():
            return result
        case PortfolioError.PortfolioNotFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=result.value)
        case InvestmentError.ColumnDoesNotExist:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=result.value)
        case _:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{portfolio_code}/investments/{investment_code}")
async def delete_investment(portfolio_code: str, investment_code: str):
    result = investment_service.delete_investment(portfolio_code, investment_code)
    match result:
        case constants.SUCCESS_RESULT:
            return {"message": "Investment deleted successfully"}
        case InvestmentError.InvestmentNotFound | PortfolioError.PortfolioNotFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result.value)
        case _:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/{portfolio_code}/investments/{investment_code}", response_model=InvestmentModel)
async def update_investment(portfolio_code: str, investment_code: str, input: InvestmentModel):
    result = investment_service.update_investment(portfolio_code, investment_code, input)
    match result:
        case InvestmentModel():
            return result
        case InvestmentError.InvestmentNotFound | PortfolioError.PortfolioNotFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result.value)
        case _:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{portfolio_code}/investments-diversification", response_model=List[AssetTypeValue])
async def get_diversification_portfolio(portfolio_code: str):
    result = investment_service.get_diversification_portfolio(portfolio_code)

    match result:
        case dict():
            return [AssetTypeValue(asset_type=asset, value=value) for asset, value in result.items()]
        case PortfolioError.PortfolioNotFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Portfolio not found."
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred."
            )


@router.get("/portfolio-consolidation/{portfolio_code}", response_model=PortfolioOverviewModel)
async def get_portfolio_consolidation(portfolio_code: str):
    portfolio_overview = investment_service.get_portfolio_overview(portfolio_code)
    if portfolio_overview is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found.")
    return portfolio_overview


@router.put("/{portfolio_code}/investments-prices")
async def update_investments_prices(portfolio_code: str):
    result = investment_service.update_stock_price(portfolio_code)
    match result:
        case constants.SUCCESS_RESULT:
            return {"message": "Investment price updated successfully"}
        case InvestmentError.InvestmentNotFound | PortfolioError.PortfolioNotFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result.value)
        case _:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
