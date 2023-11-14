from datetime import date
from typing import List
from decimal import Decimal

from src.constants import SUCCESS_RESULT
from src.investment.domain.investment_errors import OperationNotPermittedError, UnexpectedError
from src.investment.domain.models import InvestmentModel, PortfolioOverviewModel, TransactionModel
from src.investment.repository.investment_db_repository import InvestmentRepo
from src.investment.repository.portfolio_db_repository import PortfolioRepo


class InvestmentService:
    def __init__(self, portfolio_repo: PortfolioRepo, investment_repo: InvestmentRepo, stock_repo):
        self.portfolio_repo: PortfolioRepo = portfolio_repo
        self.investment_repo: InvestmentRepo = investment_repo
        self.stock_repo = stock_repo

    def create_investment(self, new_investment: InvestmentModel) -> InvestmentModel:
        self.portfolio_repo.find_by_code(new_investment.portfolio_code)
        return self.investment_repo.create(new_investment)

    def find_investment_by_code(self, portfolio_code: str, code: str) -> InvestmentModel:
        return self.investment_repo.find_by_portf_investment_code(portfolio_code, code)

    def find_all_investments(
            self, portfolio_code: str, order_by: str = None
    ) -> List[InvestmentModel]:
        """
        Retrieves all investments associated with a specific portfolio identified by its code.

        Parameters:
        portfolio_code (str): The unique identifier for the portfolio whose investments are to be retrieved.

        Returns:
        List[InvestmentModel]: A list of InvestmentModel instances representing all investments
                               associated with the specified portfolio if the portfolio exists.
        Usage:
        - Calling this function with a valid portfolio code will return all investments of that portfolio.
        - If the portfolio does not exist, it returns an error indicating that the portfolio was not found.
        - If a database error occurs, it returns a generic database error.
        """
        self.portfolio_repo.find_by_code(portfolio_code)
        return self.investment_repo.find_all_by_portfolio_code(portfolio_code, order_by)

    def delete_investment(self, portfolio_code: str, investment_code: str):
        self.portfolio_repo.find_by_code(portfolio_code)
        return self.investment_repo.delete(portfolio_code, investment_code)

    def update_investment(
            self,
            portfolio_code: str,
            investment_code: str,
            updated_investment: InvestmentModel
    ) -> InvestmentModel:
        self.portfolio_repo.find_by_code(portfolio_code)
        if investment_code != updated_investment.code:
            raise OperationNotPermittedError()
        return self.investment_repo.update(portfolio_code, investment_code, updated_investment)

    def get_portfolio_overview(self, portfolio_code: str) -> PortfolioOverviewModel:
        try:
            portfolio = self.portfolio_repo.find_by_code(portfolio_code)
            investments = self.investment_repo.find_all_by_portfolio_code(portfolio_code)

            amount_invested = Decimal(0.0)
            current_balance = Decimal(0.0)
            portfolio_yield = Decimal(0.0)
            portfolio_gross_nominal_yield = Decimal(0.0)

            for investment in investments:
                amount_invested += Decimal(investment.purchase_price * investment.quantity)
                if investment.current_average_price:
                    current_balance += Decimal(investment.current_average_price * investment.quantity)

            if len(investments) > 0:
                portfolio_yield = (current_balance - amount_invested) / amount_invested * 100
                portfolio_gross_nominal_yield = current_balance - amount_invested

            consolidation = PortfolioOverviewModel(
                code=portfolio.code,
                name=portfolio.name,
                description=portfolio.description,
                amount_invested=round(amount_invested, 2),
                current_balance=round(current_balance, 2),
                portfolio_yield=round(portfolio_yield, 1),
                portfolio_gross_nominal_yield=round(portfolio_gross_nominal_yield, 2),
            )

            return consolidation

        except Exception as e:
            raise UnexpectedError()

    def get_diversification_portfolio(self, portfolio_code: str):
        self.portfolio_repo.find_by_code(portfolio_code)
        return self.investment_repo.get_diversification_portfolio(portfolio_code)

    def update_stock_price(self, portfolio_code: str):
        investments = self.find_all_investments(portfolio_code)
        for investment in investments:
            if investment.asset_type != "STOCK":
                continue
            symbol = investment.ticker
            current_price = self.stock_repo.get_price(symbol)
            investment.current_average_price = current_price
            self.update_investment(portfolio_code, investment.code, investment)
        return SUCCESS_RESULT

    def calculate_investment_details(
            self, investment_code: str, transactions: List[TransactionModel]
    ) -> dict:
        total_quantity = 0
        total_cost = 0
        latest_price = 0
        latest_date = date.min

        for transaction in transactions:
            if transaction.investment_code == investment_code:
                total_quantity += transaction.quantity
                total_cost += transaction.quantity * transaction.price

                if transaction.date > latest_date:
                    latest_date = transaction.date
                    latest_price = transaction.price

        average_price = total_cost / total_quantity if total_quantity > 0 else 0
        investment = self.investment_repo.find_by_code(investment_code)
        investment.current_average_price = latest_price
        investment.quantity = total_quantity
        investment.purchase_price = average_price
        return self.update_investment(investment.portfolio_code, investment.code, investment)
