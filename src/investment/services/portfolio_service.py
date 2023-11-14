from typing import List, Union

from src.investment.domain.models import PortfolioModel
from src.investment.repository.portfolio_db_repository import PortfolioRepo
from src.investment.services.investment_service import InvestmentService


class PortfolioService:
    def __init__(self, portfolio_repo: PortfolioRepo, investment_service: InvestmentService):
        self.portfolio_repo: PortfolioRepo = portfolio_repo
        self.investment_service = investment_service

    def create_portfolio(self, new_portfolio: PortfolioModel) -> PortfolioModel:
        return self.portfolio_repo.create(new_portfolio)

    def update_portfolio(self, portfolio_code: str, updated_portfolio: PortfolioModel) \
            -> PortfolioModel:
        return self.portfolio_repo.update(portfolio_code, updated_portfolio)

    def delete_portfolio(self, portfolio_code: str):
        return self.portfolio_repo.delete(portfolio_code)

    def find_portfolio_by_code(self, code: str) -> PortfolioModel:
        return self.portfolio_repo.find_by_code(code)

    def find_all_portfolios(self) -> List[PortfolioModel]:
        return self.portfolio_repo.find_all()
