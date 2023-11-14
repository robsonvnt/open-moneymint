from src.investment.interface.transaction_http import NewTransactionInput
from tests.investment.prepareto_db_test import *


def test_get_all_transactions(client, db_session):
    # Adding sample portfolios to db_session as needed
    add_portfolio(db_session)
    add_investments(db_session)
    add_transactions(db_session)

    response = client.get("/portfolios/PORT100/investments/INV100/transactions")
    json_result = response.json()

    assert response.status_code == 200
    assert isinstance(json_result, list)
    assert len(json_result) == 2


def test_get_all_transactions_portfolio_not_fount(client, db_session):
    # Adding sample portfolios to db_session as needed
    add_portfolio(db_session)
    add_investments(db_session)
    add_transactions(db_session)

    response = client.get("/portfolios/non-existent-code/investments/INV100/transactions")
    assert response.status_code == 404

    response = client.get("/portfolios/PORT100/investments/non-existent-code/transactions")

    assert response.status_code == 404


def test_get_transaction(client, db_session):
    # Adding sample portfolios to db_session as needed
    add_portfolio(db_session)
    add_investments(db_session)
    add_transactions(db_session)

    response = client.get("/portfolios/PORT100/investments/INV100/transactions/TRAN101")
    assert response.status_code == 200

    result = response.json()
    assert result["code"] == "TRAN101"
    assert result["investment_code"] == "INV100"
    assert result["type"] == "BUY"
    assert result["date"] == str(date.today())
    assert result["quantity"] == 10
    assert result["price"] == 530


def test_get_transaction_error_404(client, db_session):
    # Adding sample portfolios to db_session as needed
    add_portfolio(db_session)
    add_investments(db_session)
    add_transactions(db_session)

    response = client.get("/portfolios/non-existent-code/investments/INV100/transactions/TRAN101")
    assert response.status_code == 404

    response = client.get("/portfolios/PORT100/investments/non-existent-code/transactions/TRAN101")
    assert response.status_code == 404

    response = client.get("/portfolios/PORT100/investments/INV100/transactions/non-existent-code")
    assert response.status_code == 404


def test_create_transaction(client, db_session):
    add_portfolio(db_session)
    add_investments(db_session)

    transaction_data = {
        "code": "TRAN101",
        "investment_code": "INV100",
        "type": "BUY",
        "date": str(date.today()),
        "quantity": 10,
        "price": 530
    }

    response = client.post("/portfolios/PORT100/investments/INV100/transactions", json=transaction_data)
    assert response.status_code == 200

    response = client.post("/portfolios/PORT100/investments/INV101/transactions", json=transaction_data)
    assert response.status_code == 403

    response = client.post("/portfolios/non-existent-code/investments/INV100/transactions", json=transaction_data)
    assert response.status_code == 404

    transaction_data["investment_code"] = "non-existent-code"
    response = client.post("/portfolios/PORT100/investments/non-existent-code/transactions", json=transaction_data)
    assert response.status_code == 404

    response = client.post("/portfolios/PORT100/investments/non-existent-code/transactions", json={"test": 123})
    assert response.status_code == 422

    response = client.post(
        "/portfolios/PORT100/investments/non-existent-code/transactions",
        json=transaction_data.pop("code")
    )
    assert response.status_code == 422


def test_delete_transaction(client, db_session):
    add_portfolio(db_session)
    add_investments(db_session)
    add_transactions(db_session)

    response = client.delete("/portfolios/PORT100/investments/INV101/transactions/TRAN102")
    assert response.status_code == 404

    response = client.delete("/portfolios/PORT100/investments/INV100/transactions/non-existent-code")
    assert response.status_code == 404

    response = client.delete("/portfolios/non-existent-code/investments/INV100/transactions/TRAN102")
    assert response.status_code == 404

    response = client.delete("/portfolios/PORT100/investments/non-existent-code/transactions/TRAN102")
    assert response.status_code == 404

    response = client.delete("/portfolios/PORT100/investments/INV100/transactions/TRAN102")
    assert response.status_code == 200
