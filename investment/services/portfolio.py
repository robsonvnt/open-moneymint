from typing import List, Union
from decimal import Decimal
from enum import Enum

from investment.domains import PortfolioModel, PortfolioConsolidationModel, PortfolioError
from investment.repository.portfolio_db_repositorio import PortfolioRepo
from investment.services.investment_service import InvestmentService


class PortfolioService:
    def __init__(self, portfolio_repo: PortfolioRepo, investment_service: InvestmentService):
        self.portfolio_repo: PortfolioRepo = portfolio_repo
        self.investment_service = investment_service

    def create_portfolio(self, new_portfolio: PortfolioModel) -> Union[PortfolioModel, PortfolioError]:
        return self.portfolio_repo.create(new_portfolio)

    def update_portfolio(self, portfolio_code: str, updated_portfolio: PortfolioModel) \
            -> Union[PortfolioModel, PortfolioError]:
        try:
            return self.portfolio_repo.update(portfolio_code, updated_portfolio)
        except Exception as e:
            return PortfolioError.DatabaseError

    def delete_portfolio(self, portfolio_code: str) -> Union[None, PortfolioError]:
        try:
            return self.portfolio_repo.delete(portfolio_code)
        except Exception as e:
            print(f"Error occurred: {e}")
            return PortfolioError.DatabaseError

    def find_portfolio_by_code(self, code: str) -> Union[PortfolioModel, PortfolioError]:
        try:
            return self.portfolio_repo.find_by_code(code)
        except Exception as e:
            return PortfolioError.DatabaseError

    def find_all_portfolios(self) -> List[PortfolioModel]:
        try:
            return self.portfolio_repo.find_all()
        except Exception as e:
            return PortfolioError.DatabaseError

    def consolidate_portfolio(self, portfolio_code: str) -> Union[PortfolioConsolidationModel, PortfolioError]:
        try:
            portfolio = self.find_portfolio_by_code(portfolio_code)
            if isinstance(portfolio, PortfolioError):
                return portfolio

            investments = self.investment_service.find_all_investments(portfolio_code)
            if isinstance(investments, PortfolioError):
                return investments

            amount_invested = Decimal(0)
            current_balance = Decimal(0)

            for investment in investments:
                amount_invested += Decimal(investment.purchase_price * investment.quantity)
                if investment.current_average_price:
                    current_balance += Decimal(investment.current_average_price * investment.quantity)

            portfolio_yield = ((
                                       current_balance - amount_invested) / amount_invested) * 100 if amount_invested != 0 else 0

            consolidation = PortfolioConsolidationModel(
                code=portfolio.code,
                name=portfolio.name,
                description=portfolio.description,
                amount_invested=amount_invested,
                current_balance=current_balance,
                portfolio_yield=round(portfolio_yield, 1)
            )

            return consolidation

        except Exception as e:
            return PortfolioError.Unexpected
