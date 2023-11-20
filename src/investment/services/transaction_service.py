from typing import List

from src.investment.domain.models import TransactionModel, AssetType, TransactionType, \
    InvestmentModel
from src.investment.domain.transaction_errors import TransactionNotFound, TransactionOperationNotPermitted
from src.investment.repository.transaction_db_repository import TransactionRepo
from src.investment.services.investment_service import InvestmentService


class TransactionService:
    def __init__(self, transaction_repo: TransactionRepo, investment_service: InvestmentService):
        self.transaction_repo: TransactionRepo = transaction_repo
        self.investment_service = investment_service

    def find_all(self, portfolio_code, investment_code) -> List[TransactionModel]:
        return self.transaction_repo.find_all(portfolio_code, investment_code)

    def find_by_code(self, user_code: str, portfolio_code, investment_code, trasaction_code) -> TransactionModel:
        investment = self.investment_service.find_by_code(user_code, portfolio_code, investment_code)
        transaction = self.transaction_repo.find_by_code(trasaction_code)
        if investment.code == transaction.investment_code:
            return transaction
        else:
            raise TransactionNotFound()

    def _calc_avg_purchase_price(self, old_quantity: int, old_price: float,
                                 new_quantity: int, new_price: float) -> float:
        """
        Calcula o preço médio de compra.

        :param old_quantity: Quantidade de ações antes da nova transação.
        :param old_price: Preço médio de compra antes da nova transação.
        :param new_quantity: Quantidade de ações da nova transação.
        :param new_price: Preço de compra da nova transação.
        :return: Novo preço médio de compra.
        """
        total_quantity = old_quantity + new_quantity
        if total_quantity == 0:
            return 0
        total_amount = (old_quantity * old_price) + (new_quantity * new_price)
        return total_amount / total_quantity

    def _update_stocks(self, investment: InvestmentModel, new_transaction: TransactionModel):
        match new_transaction.type:
            case TransactionType.BUY:
                old_quantity = investment.quantity
                old_avg_price = investment.purchase_price
                new_quantity = new_transaction.quantity
                new_price = new_transaction.price

                avg_price = self._calc_avg_purchase_price(old_quantity, old_avg_price,
                                                          new_quantity, new_price)
                investment.quantity += new_quantity
                investment.current_average_price = new_price
                investment.purchase_price = avg_price
            case TransactionType.SELL:

                investment.quantity -= new_transaction.quantity
                investment.current_average_price = new_transaction.price
        return investment

    def _update_fixed_income(self, investment: InvestmentModel, new_transaction: TransactionModel):
        match new_transaction.type:
            case TransactionType.INTEREST:
                investment.current_average_price += new_transaction.price
            case TransactionType.DEPOSIT:
                investment.current_average_price += new_transaction.price
                investment.purchase_price += new_transaction.price
            case TransactionType.WITHDRAWAL:
                investment.current_average_price -= new_transaction.price
                investment.purchase_price -= new_transaction.price
        return investment

    def _update_investment(
            self,
            investment: InvestmentModel,
            new_transaction: TransactionModel
    ):
        """
        Atualiza a carteira de investimentos com uma nova transação.

        :param investment: Objeto representando o investimento atual.
        :param new_transaction: Objeto representando a nova transação.
        :return: Investimento atualizado.
        """
        if investment.asset_type == AssetType.FIXED_INCOME:
            return self._update_fixed_income(investment, new_transaction)
        else:
            return self._update_stocks(investment, new_transaction)

    def create(
            self,
            user_code: str,
            portfolio_code: str,
            investment_code: str,
            new_transaction: TransactionModel,
            update_investment=True
    ) -> TransactionModel:
        if investment_code != new_transaction.investment_code:
            raise TransactionOperationNotPermitted()
        if update_investment:
            investment = self.investment_service.find_by_code(
                user_code,
                portfolio_code,
                investment_code
            )
            updated_investment = self._update_investment(investment, new_transaction)
            self.investment_service.update(
                user_code,
                portfolio_code,
                updated_investment.code,
                updated_investment
            )
        return self.transaction_repo.create(new_transaction)

    def delete(self, user_code: str, portfolio_code: str, investment_code, transaction: TransactionModel):
        """
        Deletes a specified transaction and subsequently refreshes the associated investment details.

        This method performs two main actions:
        1. Deletes the transaction specified by the 'transaction' argument from the transaction repository.
        2. Refreshes the investment details associated with the investment code of the deleted transaction.

        The refresh operation ensures that the investment details are updated to reflect the state after the transaction's deletion. This is crucial for maintaining the accuracy of investment records.

        Parameters:
            transaction (TransactionModel): The transaction to be deleted. It must contain the transaction code for deletion and the investment code for refreshing the investment details.

        Returns:
            None: This method does not return a value.

        Note: The deletion of the transaction is immediately followed by the update of the investment details to ensure data consistency. The method relies on 'transaction_repo' for the deletion operation and 'investment_service' for refreshing investment details.
        @param transaction:
        @param investment_code:
        @param portfolio_code:
        @param user_code:
        """
        investment = self.investment_service.find_by_code(user_code, portfolio_code, investment_code)
        if investment.code != transaction.investment_code:
            raise TransactionOperationNotPermitted()
        self.transaction_repo.delete(transaction.code)

        transactions = self.transaction_repo.find_all(portfolio_code, investment.code)
        self.investment_service. \
            refresh_investment_details(user_code, investment_code, transactions)
