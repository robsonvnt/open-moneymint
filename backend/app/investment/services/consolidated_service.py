from datetime import date

from investment.domain.models import ConsolidatedPortfolioModel
from investment.repository.consolidated_balance_db_repository import ConsolidatedBalanceRepo
from investment.services.investment_service import InvestmentService


class ConsolidatedPortfolioService:
    def __init__(self, cpb_repo: ConsolidatedBalanceRepo, investment_service):
        self.cpb_repo: ConsolidatedBalanceRepo = cpb_repo
        self.investment_service: InvestmentService = investment_service

    def filter_by_date_range(self, portfolio_code: str, start_date=None, end_date=None):
        return self.cpb_repo.filter_by_date_range(portfolio_code, start_date, end_date)

    def consolidate_portfolio(
            self, user_code: str, portfolio_code: str
    ) -> ConsolidatedPortfolioModel:
        result = self.investment_service.get_portfolio_overview(user_code, portfolio_code)
        cpm = ConsolidatedPortfolioModel(
            portfolio_code=result.code,
            date=date.today(),
            balance=result.current_balance,
            amount_invested=result.amount_invested,
        )
        return self.cpb_repo.create_or_update(cpm)
