from investment.repository.factory import RepositoryFactory
from investment.repository.transaction_db_repository import TransactionRepo
from investment.services.consolidated_service import ConsolidatedPortfolioService
from investment.services.investment_service import InvestmentService
from investment.services.portfolio_service import PortfolioService
from investment.services.transaction_service import TransactionService


class ServiceFactory:
    @staticmethod
    def create_portfolio_service(session=None) -> PortfolioService:
        portfolio_repo = RepositoryFactory.create_portfolio_repo(session)
        investment_service = ServiceFactory.create_investment_service(session)
        return PortfolioService(portfolio_repo, investment_service)

    @staticmethod
    def create_investment_service(session=None) -> InvestmentService:
        portfolio_repo = RepositoryFactory.create_portfolio_repo(session)
        investment_repo = RepositoryFactory.create_investment_repo(session)
        stock_repo = RepositoryFactory.create_stock_repo()
        transaction_repo = TransactionRepo(session)
        return InvestmentService(portfolio_repo, investment_repo, stock_repo, transaction_repo)

    @staticmethod
    def create_consolidated_balance_service(session=None) -> ConsolidatedPortfolioService:
        consolidated_balance_repo = RepositoryFactory.consolidated_balance_repo(session)
        investment_service = ServiceFactory.create_investment_service(session)
        return ConsolidatedPortfolioService(consolidated_balance_repo, investment_service)

    @staticmethod
    def create_transaction_service(session=None) -> TransactionService:
        investment_service = ServiceFactory.create_investment_service(session)
        transaction_repo = TransactionRepo(session)
        return TransactionService(transaction_repo, investment_service)
