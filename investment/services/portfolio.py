from typing import List, Union
from decimal import Decimal
from enum import Enum

from investment.domains import PortfolioModel, PortfolioConsolidationModel, PortfolioError
from investment.repository.portfolio_db_repositorio import PortfolioRepo
from investment.services.investment_service import InvestmentService


class PortfolioService:
    def __init__(self, portfolio_repo: PortfolioRepo, investment_service: InvestmentService):
        self.portfolio_repo: PortfolioRepo = portfolio_repo
        self.investment_service = investment_service

    def create_portfolio(self, new_portfolio: PortfolioModel) -> Union[PortfolioModel, PortfolioError]:
        return self.portfolio_repo.create(new_portfolio)

    def update_portfolio(self, portfolio_code: str, updated_portfolio: PortfolioModel) \
            -> Union[PortfolioModel, PortfolioError]:
        try:
            return self.portfolio_repo.update(portfolio_code, updated_portfolio)
        except Exception as e:
            return PortfolioError.DatabaseError

    def delete_portfolio(self, portfolio_code: str) -> Union[None, PortfolioError]:
        try:
            return self.portfolio_repo.delete(portfolio_code)
        except Exception as e:
            print(f"Error occurred: {e}")
            return PortfolioError.DatabaseError

    def find_portfolio_by_code(self, code: str) -> Union[PortfolioModel, PortfolioError]:
        try:
            return self.portfolio_repo.find_by_code(code)
        except Exception as e:
            return PortfolioError.DatabaseError

    def find_all_portfolios(self) -> List[PortfolioModel]:
        try:
            return self.portfolio_repo.find_all()
        except Exception as e:
            return PortfolioError.DatabaseError

