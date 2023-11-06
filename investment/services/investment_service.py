from typing import List, Union
from decimal import Decimal
from enum import Enum

from investment.domains import InvestmentModel, PortfolioConsolidationModel, InvestmentError, PortfolioError, \
    PortfolioModel
from investment.repository.investment_db_repositorio import InvestmentRepo
from investment.repository.portfolio_db_repositorio import PortfolioRepo


class InvestmentService:
    def __init__(self, portfolio_repo: PortfolioRepo, investment_repo: InvestmentRepo):
        self.portfolio_repo: PortfolioRepo = portfolio_repo
        self.investment_repo: InvestmentRepo = investment_repo

    def create_investment(self, new_investment: InvestmentModel) -> Union[InvestmentModel, InvestmentError]:
        result = self.portfolio_repo.find_by_code(new_investment.portfolio_code)
        match result:
            case PortfolioModel():
                return self.investment_repo.create(new_investment)
            case _:
                return PortfolioError.PortfolioNotFound

    def find_investment_by_code(self, portfolio_code: str, code: str) -> Union[InvestmentModel, InvestmentError]:
        try:
            return self.investment_repo.find_by_code(portfolio_code, code)
        except Exception as e:
            return InvestmentError.DatabaseError

    def find_all_investments(self, portfolio_code: str) -> List[InvestmentModel]:
        """
        Retrieves all investments associated with a specific portfolio identified by its code.

        Parameters:
        portfolio_code (str): The unique identifier for the portfolio whose investments are to be retrieved.

        Returns:
        List[InvestmentModel]: A list of InvestmentModel instances representing all investments
                               associated with the specified portfolio if the portfolio exists.
        PortfolioError.PortfolioNotFound: If no portfolio with the specified code is found.
        InvestmentError.DatabaseError: If an exception occurs while interacting with the database.

        Usage:
        - Calling this function with a valid portfolio code will return all investments of that portfolio.
        - If the portfolio does not exist, it returns an error indicating that the portfolio was not found.
        - If a database error occurs, it returns a generic database error.
        """
        result = self.portfolio_repo.find_by_code(portfolio_code)
        match result:
            case PortfolioModel():
                return self.investment_repo.find_all_by_portfolio_code(portfolio_code)
            case PortfolioError.PortfolioNotFound:
                return PortfolioError.PortfolioNotFound
            case InvestmentError.Unexpected:
                return InvestmentError.Unexpected

    def delete_investment(self, portfolio_code: str, investment_code: str) -> Union[None, InvestmentError]:
        result = self.portfolio_repo.find_by_code(portfolio_code)
        if result == PortfolioError.PortfolioNotFound:
            return PortfolioError.PortfolioNotFound
        return self.investment_repo.delete(portfolio_code, investment_code)

    def update_investment(self, portfolio_code: str, investment_code: str, updated_investment: InvestmentModel):
        result = self.portfolio_repo.find_by_code(portfolio_code)
        if result == PortfolioError.PortfolioNotFound:
            return PortfolioError.PortfolioNotFound
        return self.investment_repo.update(portfolio_code, investment_code, updated_investment)

    def consolidate_portfolio(self, portfolio_code: str) -> Union[PortfolioConsolidationModel, InvestmentError]:
        try:
            portfolio = self.portfolio_repo.find_by_code(portfolio_code)
            if isinstance(portfolio, InvestmentError):
                return portfolio

            investments = self.investment_repo.find_all_by_portfolio_code(portfolio_code)
            if isinstance(investments, InvestmentError):
                return investments

            amount_invested = 0.0
            current_balance = 0.0

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
            return InvestmentError.Unexpected

    def get_diversification_portfolio(self, portfolio_code: str):
        result = self.portfolio_repo.find_by_code(portfolio_code)
        if result == PortfolioError.PortfolioNotFound:
            return PortfolioError.PortfolioNotFound
        return self.investment_repo.get_diversification_portfolio(portfolio_code)