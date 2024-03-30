from datetime import date
from decimal import Decimal
from typing import List

from constants import SUCCESS_RESULT
from investment.domain.investment_errors import OperationNotPermittedError, UnexpectedError
from investment.domain.models import InvestmentModel, PortfolioOverviewModel, TransactionModel, TransactionType, \
    AssetType
from investment.domain.transaction_errors import TransactionInvalidType, TransactionOperationNotPermitted
from investment.repository.investment_db_repository import InvestmentRepo
from investment.repository.portfolio_db_repository import PortfolioRepo
from investment.repository.transaction_db_repository import TransactionRepo


class InvestmentService:
    def __init__(self, portfolio_repo: PortfolioRepo, investment_repo: InvestmentRepo,
                 stock_repo, transaction_repo: TransactionRepo = None):
        self.portfolio_repo: PortfolioRepo = portfolio_repo
        self.investment_repo: InvestmentRepo = investment_repo
        self.stock_repo = stock_repo
        self.transaction_repo: TransactionRepo = transaction_repo

    def create(self, user_code: str, new_investment: InvestmentModel) -> InvestmentModel:
        self.portfolio_repo.find_by_code(user_code, new_investment.portfolio_code)
        created_investment = self.investment_repo.create(new_investment)

        # Criar transaction
        # Todo create test case
        if self.transaction_repo:
            transaction_type = TransactionType.BUY
            if created_investment.asset_type == AssetType.FIXED_INCOME:
                transaction_type = TransactionType.DEPOSIT
            transaction = TransactionModel(
                code=None, investment_code=created_investment.code, type=transaction_type,
                date=created_investment.purchase_date, quantity=created_investment.quantity,
                price=created_investment.purchase_price
            )
            self.transaction_repo.create(transaction)

        return created_investment

    def find_by_code(self, user_code: str, portfolio_code: str, code: str) -> InvestmentModel:
        portfolio = self.portfolio_repo.find_by_code(user_code, portfolio_code)
        return self.investment_repo.find_by_portf_investment_code(portfolio.code, code)

    def find_all(
            self, user_code: str, portfolio_code: str, order_by: str = None
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
        self.portfolio_repo.find_by_code(user_code, portfolio_code)
        return self.investment_repo.find_all_by_portfolio_code(portfolio_code, order_by)

    def delete(self, user_code: str, portfolio_code: str, investment_code: str):
        self.portfolio_repo.find_by_code(user_code, portfolio_code)
        return self.investment_repo.delete(portfolio_code, investment_code)

    def update(
            self,
            user_code: str,
            portfolio_code: str,
            investment_code: str,
            updated_investment: InvestmentModel
    ) -> InvestmentModel:
        self.portfolio_repo.find_by_code(user_code, portfolio_code)
        if investment_code != updated_investment.code:
            raise OperationNotPermittedError()
        return self.investment_repo.update(portfolio_code, investment_code, updated_investment)

    def get_portfolio_overview(self, user_code: str, portfolio_code: str) -> PortfolioOverviewModel:
        try:
            portfolio = self.portfolio_repo.find_by_code(user_code, portfolio_code)
            investments = self.investment_repo.find_all_by_portfolio_code(portfolio_code)

            amount_invested = Decimal(0.0)
            current_balance = Decimal(0.0)
            portfolio_yield = Decimal(0.0)
            portfolio_gross_nominal_yield = Decimal(0.0)

            for investment in investments:
                amount_invested += Decimal(investment.purchase_price * investment.quantity)
                if investment.current_average_price:
                    current_balance += Decimal(investment.current_average_price * investment.quantity)

            if len(investments) > 0 and amount_invested > 0:
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

    def get_diversification_portfolio(self, user_code: str, portfolio_code: str):
        self.portfolio_repo.find_by_code(user_code, portfolio_code)
        return self.investment_repo.get_diversification_portfolio(portfolio_code)

    def update_stock_price(self, user_code: str, portfolio_code: str):
        investments = self.find_all(user_code, portfolio_code)
        for investment in investments:
            if investment.asset_type not in (AssetType.STOCK, AssetType.REIT):
                continue
            symbol = investment.ticker
            current_price = self.stock_repo.get_price(symbol)
            investment.current_average_price = current_price
            self.update(user_code, portfolio_code, investment.code, investment)
        return SUCCESS_RESULT

    def _refresh_stock_price(
            self, user_code: str, investment: InvestmentModel, transactions: List[TransactionModel]
    ):
        total_quantity = 0
        total_sold = 0
        total_cost = 0
        latest_price = 0
        latest_date = date.min

        for transaction in transactions:
            if transaction.type == TransactionType.BUY:
                total_quantity += transaction.quantity
                total_cost += transaction.quantity * transaction.price
            elif transaction.type == TransactionType.SELL:
                total_sold += transaction.quantity
            else:
                raise TransactionInvalidType()

            if transaction.date > latest_date:
                latest_date = transaction.date
                latest_price = transaction.price

        average_price = total_cost / total_quantity if total_quantity > 0 else 0
        investment.current_average_price = latest_price
        investment.quantity = total_quantity - total_sold
        investment.purchase_price = round(average_price * 100) / 100

        if investment.quantity < 0:
            raise TransactionOperationNotPermitted("Quantity cannot be negative")
        return self.update(user_code, investment.portfolio_code, investment.code, investment)

    def _refresh_fixed_income_balance(
            self, user_code: str, investment: InvestmentModel, transactions: List[TransactionModel]
    ):
        investment
        balance = 0
        total_invested = 0
        for transaction in transactions:
            if transaction.type == TransactionType.DEPOSIT:
                balance += transaction.price
                total_invested += transaction.price
            elif transaction.type == TransactionType.INTEREST:
                balance += transaction.price
            elif transaction.type == TransactionType.WITHDRAWAL:
                balance -= transaction.price
                total_invested -= transaction.price
            else:
                raise TransactionInvalidType()

        investment.current_average_price = balance
        investment.purchase_price = total_invested
        return self.update(user_code, investment.portfolio_code, investment.code, investment)

    def refresh_investment_details(
            self, user_code: str, investment_code: str, transactions: List[TransactionModel]
    ) -> InvestmentModel:
        investment: InvestmentModel = self.investment_repo.find_by_code(investment_code)
        if investment.asset_type in (AssetType.STOCK, AssetType.REIT):
            return self._refresh_stock_price(user_code, investment, transactions)
        else:
            return self._refresh_fixed_income_balance(user_code, investment, transactions)
