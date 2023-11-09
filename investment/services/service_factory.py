import os

from investment.repository.consolidated_balance_db_repository import ConsolidatedBalanceRepo
from investment.repository.investment_db_repository import InvestmentRepo
from investment.repository.portfolio_db_repository import PortfolioRepo
from investment.repository.repository_factory import RepositoryFactory
from investment.services.consolidated_service import ConsolidatedPortfolioService
from investment.services.investment_service import InvestmentService
from investment.services.portfolio import PortfolioService

class ServiceFactory:
    @staticmethod
    def create_portfolio_service() -> PortfolioService:
        portfolio_repo = RepositoryFactory.create_portfolio_repo()
        investment_service = ServiceFactory.create_investment_service()
        return PortfolioService(portfolio_repo, investment_service)

    @staticmethod
    def create_investment_service() -> InvestmentService:
        portfolio_repo = RepositoryFactory.create_portfolio_repo()
        investment_repo = RepositoryFactory.create_investment_repo()
        stock_repo = RepositoryFactory.create_stock_repo()
        return InvestmentService(portfolio_repo, investment_repo,stock_repo)

    @staticmethod
    def create_consolidated_balance_service() -> ConsolidatedPortfolioService:
        consolidated_balance_repo = RepositoryFactory.consolidated_balance_repo()
        investment_service = ServiceFactory.create_investment_service()
        return ConsolidatedPortfolioService(consolidated_balance_repo, investment_service)
# Uso:
# portfolio_service = PortfolioServiceFactory.create()
