import os

from investment.repository.consolidated_balance_db_repositorio import ConsolidatedBalanceRepo
from investment.repository.investment_db_repositorio import InvestmentRepo
from investment.repository.portfolio_db_repositorio import PortfolioRepo
from investment.services.consolidated_service import ConsolidatedPortfolioService
from investment.services.investment_service import InvestmentService
from investment.services.portfolio import PortfolioService

db_url = os.environ.get('DATABASE_URL')


class ServiceFactory:
    @staticmethod
    def create_portfolio_service() -> PortfolioService:
        portfolio_repo = PortfolioRepo(db_url)
        investment_service = ServiceFactory.create_investment_service()
        return PortfolioService(portfolio_repo, investment_service)

    @staticmethod
    def create_investment_service() -> InvestmentService:
        portfolio_repo = PortfolioRepo(db_url)
        investment_repo = InvestmentRepo(db_url)
        return InvestmentService(portfolio_repo, investment_repo)

    @staticmethod
    def create_consolidated_balance_service() -> ConsolidatedPortfolioService:
        consolidated_balance_repo = ConsolidatedBalanceRepo(db_url)
        investment_service = ServiceFactory.create_investment_service()
        return ConsolidatedPortfolioService(consolidated_balance_repo, investment_service)
# Uso:
# portfolio_service = PortfolioServiceFactory.create()
