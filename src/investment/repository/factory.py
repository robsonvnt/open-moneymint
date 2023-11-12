import os

from src.investment.repository.consolidated_balance_db_repository import ConsolidatedBalanceRepo
from src.investment.repository.db.db_connection import get_db_session
from src.investment.repository.investment_db_repository import InvestmentRepo
from src.investment.repository.portfolio_db_repository import PortfolioRepo
from src.investment.repository.stock_repository import BrApiDevRepository

db_url = os.environ.get('DATABASE_URL')


class RepositoryFactory:

    @staticmethod
    def create_portfolio_repo(session=None) -> PortfolioRepo:
        if session:
            return PortfolioRepo(session)
        session = get_db_session(db_url)
        return PortfolioRepo(session)


    @staticmethod
    def create_investment_repo(session=None) -> InvestmentRepo:
        if session:
            return InvestmentRepo(session)
        session = get_db_session(db_url)
        return InvestmentRepo(session)

    @staticmethod
    def consolidated_balance_repo(session=None) -> ConsolidatedBalanceRepo:
        if session:
            return ConsolidatedBalanceRepo(session)
        session = get_db_session(db_url)
        return ConsolidatedBalanceRepo(session)

    @staticmethod
    def create_stock_repo() -> BrApiDevRepository:
        api_key = os.getenv("BRAPI_DEV")
        return BrApiDevRepository(api_key)
