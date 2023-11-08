
from investment.repository.consolidated_balance_db_repositorio import ConsolidatedBalanceRepo
from investment.services.investment_service import InvestmentService


class ConsolidatedPortfolioService:
    def __init__(self, cpb_repo: ConsolidatedBalanceRepo, investment_service):
        self.cpb_repo: ConsolidatedBalanceRepo = cpb_repo
        self.investment_service: InvestmentService = investment_service

    def filter_by_date_range(self, portfolio_code, start_date=None, end_date=None):
        return self.cpb_repo.filter_by_date_range(portfolio_code, start_date, end_date)

    def consolidate_portfolio(self, portfolio_code: str):
        result = self.investment_service.get_portfolio_overview(portfolio_code)
        self.cpb_repo.create(result)
        return result


