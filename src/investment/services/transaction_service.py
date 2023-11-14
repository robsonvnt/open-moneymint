from src.investment.domain.models import TransactionModel, AssetType, TransactionType, \
    InvestmentModel
from src.investment.repository.transaction_db_repository import TransactionRepo
from src.investment.services.investment_service import InvestmentService


class TransactionService:
    def __init__(self, transaction_repo: TransactionRepo, investment_service: InvestmentService):
        self.transaction_repo: TransactionRepo = transaction_repo
        self.investment_service = investment_service

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
            portfolio_code: str,
            new_transaction: TransactionModel,
            update_investment=True
    ) -> TransactionModel:
        if update_investment:
            investment = self.investment_service.find_investment_by_code(
                portfolio_code,
                new_transaction.investment_code
            )
            updated_investment = self._update_investment(investment, new_transaction)
            self.investment_service.update_investment(
                portfolio_code,
                updated_investment.code,
                updated_investment
            )
        return self.transaction_repo.create(new_transaction)

    def delete(
            self,
            portfolio_code: str,
            transaction: TransactionModel
    ) -> TransactionModel:
        investment = self.investment_service.find_investment_by_code(
            portfolio_code,
            transaction.investment_code
        )
        if investment.asset_type == AssetType.FIXED_INCOME:
            investment.purchase_price -= transaction.price
            investment.current_average_price -= transaction.price
        else:
            investment.quantity -= transaction.quantity

        self.investment_service.update_investment(
            portfolio_code, investment.code, investment
        )
        return self.transaction_repo.delete(transaction.code)
