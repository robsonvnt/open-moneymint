from tests.investment.prepareto_db_test import *


def test_create_investment(client, db_session):
    add_portfolio(db_session)
    add_investments(db_session)
    db_session.query(Portfolio).all()

    response = client.get("/portfolios/PORT100/investments")
    json_result = response.json()

    assert response.status_code == 200
    assert len(json_result) == 4


