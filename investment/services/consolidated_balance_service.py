
from investment.repository.consolidated_balance_db_repositorio import ConsolidatedBalanceRepo


class ConsolidatedPortfolioService:
    def __init__(self, cpb_repo: ConsolidatedBalanceRepo):
        self.cpb_repo: ConsolidatedBalanceRepo = cpb_repo

    def filter_by_date_range(self, portfolio_code, start_date=None, end_date=None):
        return self.cpb_repo.filter_by_date_range(portfolio_code, start_date, end_date)

