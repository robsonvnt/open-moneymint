from tests.investment.prepareto_db_test import *
from sqlalchemy.orm.exc import NoResultFound


def test_get_all_investment(client, db_session):
    add_portfolio(db_session)
    add_investments(db_session)

    response = client.get("/portfolios/PORT100/investments")
    json_result = response.json()

    assert response.status_code == 200
    assert len(json_result) == 4


def test_create_investment(client, db_session):
    add_portfolio(db_session)
    add_investments(db_session)

    new_investment_data = {
        "portfolio_code": "PORT100",
        "asset_type": "STOCK",
        "ticker": "AAPL",
        "quantity": 50,
        "purchase_price": 500.00,
        "current_average_price": 110.00,
        "purchase_date": "2023-01-01"
    }

    response = client.post("/portfolios/PORT100/investments", json=new_investment_data)
    assert response.status_code == 200
    json_result = response.json()

    investment_created: Investment = db_session.query(Investment).filter(Investment.code == json_result["code"]).one()
    assert investment_created.ticker == 'AAPL'
    assert investment_created.quantity == 50


def test_get_investment(client, db_session):
    add_portfolio(db_session)
    add_investments(db_session)
    response = client.get("/portfolios/PORT100/investments/INV101")
    assert response.status_code == 200
    assert response.json()["ticker"] == "MSFT"


def test_delete_investment(client, db_session):
    add_portfolio(db_session)
    add_investments(db_session)
    response = client.delete("/portfolios/PORT100/investments/INV101")

    assert response.status_code == 200

    with pytest.raises(NoResultFound) as exc_info:
        db_session.query(Investment).filter(Investment.code == "INV101").one()
    assert exc_info.type == NoResultFound


def test_update_investment(client, db_session):
    add_portfolio(db_session)
    add_investments(db_session)
    updated_data = {
        "code": "INV102",
        "portfolio_code": "PORT100",
        "asset_type": "STOCK",
        "ticker": "ticker_test",
        "quantity": 50,
        "purchase_price": 500.00,
        "current_average_price": 110.00,
        "purchase_date": "2023-01-01"
    }

    response = client.put("/portfolios/PORT100/investments/INV102", json=updated_data)
    assert response.status_code == 200

    investment = db_session.query(Investment).filter(Investment.code == "INV102").one()
    assert investment.ticker == "ticker_test"

    # Aleração de código não é permitida, teste deve retornar 403
    updated_data["code"] = "other_code"
    response = client.put("/portfolios/PORT100/investments/INV102", json=updated_data)
    assert response.status_code == 403


def test_get_diversification_portfolio(client, db_session):
    add_portfolio(db_session)
    add_investments(db_session)
    response = client.get("/portfolios/PORT100/investments-diversification")
    assert response.status_code == 200

    assert response.json()[0]["asset_type"] == "FIXED_INCOME"
    assert response.json()[0]["value"] == 6075.00
    assert response.json()[1]["asset_type"] == "STOCK"
    assert response.json()[1]["value"] == 38200.0


def test_update_investments_prices(client, db_session):
    add_portfolio(db_session)
    add_investments(db_session)

    response = client.put("/portfolios/PORT100/investments-prices", json={})
    assert response.status_code == 200

    investment = db_session.query(Investment).filter(Investment.code == "INV100").one()
    assert investment.current_average_price == 99.99
