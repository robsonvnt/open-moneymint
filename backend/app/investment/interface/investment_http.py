from datetime import date
from typing import List, Optional

from fastapi import HTTPException, status, APIRouter, Depends
from pydantic import BaseModel

from auth.user import User, get_current_user
from investment.domain.investment_errors import InvestmentNotFound, OperationNotPermittedError, \
    ColumnDoesNotExistError
from investment.domain.models import InvestmentModel, PortfolioOverviewModel, AssetType
from investment.domain.portfolio_erros import PortfolioNotFound
from investment.repository.db.db_connection import get_db_session
from investment.services.service_factory import ServiceFactory

router = APIRouter()


class NewInvestmentInput(BaseModel):
    portfolio_code: str
    asset_type: AssetType
    ticker: str
    quantity: float
    purchase_price: float
    current_average_price: Optional[float]
    purchase_date: date


class AssetTypeValue(BaseModel):
    asset_type: str
    value: float


@router.post("/{portfolio_code}/investments", response_model=InvestmentModel)
async def create_investment(
        portfolio_code,
        new_investment_form_data: NewInvestmentInput,
        db_session=Depends(get_db_session),
        current_user=Depends(get_current_user)
):
    try:
        investment_service = ServiceFactory.create_investment_service(db_session)
        if not portfolio_code == new_investment_form_data.portfolio_code:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Portfolio code does not match.")
        investment_model = InvestmentModel(code=None, **new_investment_form_data.model_dump())
        return investment_service.create(current_user.code, investment_model)

    except PortfolioNotFound as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to retrieve investments.")


@router.get("/{portfolio_code}/investments/{investment_code}", response_model=InvestmentModel)
async def get_investment(
        portfolio_code: str,
        investment_code: str,
        db_session=Depends(get_db_session),
        current_user=Depends(get_current_user)
):
    try:
        investment_service = ServiceFactory.create_investment_service(db_session)
        return investment_service.find_by_code(current_user.code, portfolio_code, investment_code)
    except InvestmentNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))


@router.get("/{portfolio_code}/investments", response_model=List[InvestmentModel])
async def get_all_investments(
        portfolio_code: str,
        order_by: str = None,
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    """
    Recupera todos os investimentos associados a um determinado código de portfólio.

    Este endpoint permite a recuperação de uma lista de investimentos filtrada pelo código do portfólio.
    Os investimentos podem app ordenados com base em qualquer coluna disponível, de forma ascendente ou descendente.

    Parâmetros:
    - portfolio_code (str): O código do portfólio para o qual os investimentos são buscados.
    - order_by (str, opcional): Parâmetro de ordenação para os resultados.
      Deve app o nome da coluna pelo qual ordenar. Para ordenação ascendente, forneça apenas o nome da coluna.
      Para ordenação descendente, adicione ".desc" após o nome da coluna (por exemplo, "purchase_date.desc").

    Retornos:
    - Lista de InvestmentModel: Uma lista de modelos de investimento correspondentes ao código do portfólio fornecido.
    - HTTP 404 Not Found: Erro levantado se o portfólio especificado não for encontrado.
    - HTTP 400 Bad Request: Erro levantado se o parâmetro 'order_by' especificar uma coluna que não existe.
    - HTTP 500 Internal Server Error: Erro levantado para qualquer outra falha no servidor.

    Exceções são tratadas para identificar portfólios não encontrados, colunas de ordenação inválidas e erros gerais de
     servidor,
    proporcionando uma resposta apropriada ao cliente.
    """
    try:
        investment_service = ServiceFactory.create_investment_service(db_session)
        result = investment_service.find_all(current_user.code, portfolio_code, order_by)
        return result
    except InvestmentNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(e))
    except ColumnDoesNotExistError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))


@router.delete("/{portfolio_code}/investments/{investment_code}")
async def delete_investment(
        portfolio_code: str,
        investment_code: str,
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    try:
        investment_service = ServiceFactory.create_investment_service(db_session)
        investment_service.delete(current_user.code, portfolio_code, investment_code)
        return {"message": "Investment deleted successfully"}
    except InvestmentNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))


@router.put("/{portfolio_code}/investments/{investment_code}", response_model=InvestmentModel)
async def update_investment(
        portfolio_code: str,
        investment_code: str,
        investment_data: InvestmentModel,
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    try:
        investment_service = ServiceFactory.create_investment_service(db_session)
        return investment_service.update(current_user.code, portfolio_code, investment_code, investment_data)
    except OperationNotPermittedError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except PortfolioNotFound | InvestmentNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{portfolio_code}/investments-diversification", response_model=List[AssetTypeValue])
async def get_diversification_portfolio(
        portfolio_code: str,
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    try:
        investment_service = ServiceFactory.create_investment_service(db_session)
        result = investment_service.get_diversification_portfolio(current_user.code, portfolio_code)
        return [AssetTypeValue(asset_type=asset, value=value) for asset, value in result.items()]
    except PortfolioNotFound | InvestmentNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/portfolio-consolidation/{portfolio_code}", response_model=PortfolioOverviewModel)
async def get_portfolio_consolidation(
        portfolio_code: str,
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    investment_service = ServiceFactory.create_investment_service(db_session)
    portfolio_overview = investment_service.get_portfolio_overview(
        current_user.code, portfolio_code
    )
    if portfolio_overview is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found.")
    return portfolio_overview


@router.put("/{portfolio_code}/investments-prices")
async def update_investments_prices(
        portfolio_code: str,
        db_session=Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    try:
        investment_service = ServiceFactory.create_investment_service(db_session)
        investment_service.update_stock_price(current_user.code, portfolio_code)
        return {"message": "Investment price updated successfully"}
    except PortfolioNotFound | InvestmentNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
