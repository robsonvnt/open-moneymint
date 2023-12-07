from investment.domain.investment_errors import ColumnDoesNotExistError
from investment.repository.investment_db_repository import InvestmentRepo
from investment.repository.prepareto_db_test import *


def test_find_all_by_portfolio_code_with_data(db_session):
    """
    Testa se a função retorna os investimentos corretos para um dado código de portfólio.
    """
    add_investments(db_session)
    investment_repo = InvestmentRepo(db_session)

    results = investment_repo.find_all_by_portfolio_code("PORT100")
    assert len(results) == 4
    assert results[0].ticker == "AAPL"
    assert results[1].ticker == "MSFT"


def test_find_all_by_portfolio_code_with_order_by(db_session):
    """
    Testa se a função retorna os investimentos corretos e ordenados por purchase_price para um dado código de portfólio.
    """
    # Adicionar dados de teste
    add_investments(db_session)
    investment_repo = InvestmentRepo(db_session)

    results = investment_repo.find_all_by_portfolio_code("PORT100", order_by="purchase_price")
    assert results[0].code == "INV103"
    assert results[3].code == "INV100"

    # Testando em ordem decrescente
    results = investment_repo.find_all_by_portfolio_code("PORT100", order_by="purchase_price.desc")
    assert results[0].code == "INV100"
    assert results[3].code == "INV103"


def test_find_all_by_portfolio_code_with_order_by_non_existent_column(db_session):
    """
    Testa se a função retorna erro por não existir a coluna a app ordenada.
    """
    # Adicionar dados de teste
    add_investments(db_session)
    investment_repo = InvestmentRepo(db_session)

    with pytest.raises(ColumnDoesNotExistError):
        investment_repo.find_all_by_portfolio_code("PORT100", order_by="non-existent column")


# def test_find_all_by_portfolio_code_empty(db_session):
#     """
#     Testa se a função retorna uma lista vazia quando não há investimentos correspondentes.
#     """
#     investment_repo = InvestmentRepo(db_session)
#     results = investment_repo.find_all_by_portfolio_code("PORT100")
#     assert results == []
#     assert len(results) == 0
