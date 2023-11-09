import os

from investment.repository.consolidated_balance_db_repository import ConsolidatedBalanceRepo
from investment.repository.db_connection import get_db_session
from investment.repository.investment_db_repository import InvestmentRepo
from investment.repository.portfolio_db_repository import PortfolioRepo

db_url = os.environ.get('DATABASE_URL')


class RepositoryFactory:

    @staticmethod
    def create_portfolio_repo() -> PortfolioRepo:
        return PortfolioRepo(db_url)

    @staticmethod
    def create_investment_repo() -> InvestmentRepo:
        return InvestmentRepo(db_url)

    @staticmethod
    def consolidated_balance_repo() -> ConsolidatedBalanceRepo:
        session = get_db_session(db_url)
        return ConsolidatedBalanceRepo(session)