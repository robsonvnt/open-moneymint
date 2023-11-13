from src.investment.domains import TransactionModel, TransactionError, AssetType, TransactionType, InvestmentModel, \
    InvestmentError
from src.investment.repository.transaction_db_repository import TransactionRepo
from src.investment.services.investment_service import InvestmentService


class TransactionService:
    def __init__(self, transaction_repo: TransactionRepo, investment_service: InvestmentService):
        self.transaction_repo: TransactionRepo = transaction_repo
        self.investment_service = investment_service

    def calc_avg_purchase_price(self, old_quantity: int, old_price: float,
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

                avg_price = self.calc_avg_purchase_price(old_quantity, old_avg_price,
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

    def update_investment(
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
            self._update_fixed_income(investment, new_transaction)
        else:
            return self._update_stocks(investment, new_transaction)
        return investment

    def create(
            self,
            portfolio_code: str,
            new_transaction: TransactionModel
    ) -> TransactionModel | TransactionError | InvestmentError:
        investment = self.investment_service.find_investment_by_code(
            portfolio_code,
            new_transaction.investment_code
        )
        match investment:
            case InvestmentError.InvestmentNotFound:
                return InvestmentError.InvestmentNotFound
            case InvestmentModel():
                updated_investment = self.update_investment(investment, new_transaction)
                result_update = self.investment_service.update_investment(
                    portfolio_code,
                    updated_investment.code,
                    updated_investment
                )
                if not isinstance(result_update, InvestmentModel):
                    return TransactionError.Unexpected
                return self.transaction_repo.create(new_transaction)
            case _:
                return TransactionError.Unexpected
