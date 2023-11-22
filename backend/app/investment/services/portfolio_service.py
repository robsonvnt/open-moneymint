from typing import List, Union

from investment.domain.models import PortfolioModel
from investment.repository.portfolio_db_repository import PortfolioRepo
from investment.services.investment_service import InvestmentService


class PortfolioService:
    def __init__(self, portfolio_repo: PortfolioRepo, investment_service: InvestmentService):
        self.portfolio_repo: PortfolioRepo = portfolio_repo
        self.investment_service = investment_service

    def create(self, user_code: str, new_portfolio: PortfolioModel) -> PortfolioModel:
        return self.portfolio_repo.create(user_code, new_portfolio)

    def update(self, user_code: str, portfolio_code: str, updated_portfolio: PortfolioModel) \
            -> PortfolioModel:
        return self.portfolio_repo.update(user_code, portfolio_code, updated_portfolio)

    def delete(self, user_code: str, portfolio_code: str):
        return self.portfolio_repo.delete(user_code, portfolio_code)

    def find_by_code(self, user_code: str, code: str) -> PortfolioModel:
        return self.portfolio_repo.find_by_code(user_code, code)

    def find_all(self, user_code) -> List[PortfolioModel]:
        return self.portfolio_repo.find_all(user_code)
