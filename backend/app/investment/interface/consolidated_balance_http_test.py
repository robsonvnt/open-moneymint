from investment.repository.prepareto_db_test import *
from fastapi import APIRouter

router = APIRouter()


def test_get_consolidated_balance(client, db_session):
    add_portfolio(db_session)
    add_investments(db_session)
    add_consolidated_portfolio(db_session)

    response = client.get("/portfolios/PORT100/consolidations")
    json_result = response.json()

    assert response.status_code == 200
    assert len(json_result) == 4

    # Teste com filtro start date
    response = client.get("/portfolios/PORT100/consolidations?start_date=2023-02-01")
    json_result = response.json()

    assert response.status_code == 200
    assert len(json_result) == 3

    # Teste com filtro end date
    response = client.get("/portfolios/PORT100/consolidations?end_date=2023-02-01")
    json_result = response.json()

    assert response.status_code == 200
    assert len(json_result) == 2

    # Teste com filtro end e start date
    response = client.get("/portfolios/PORT100/consolidations?start_date=2023-01-10&end_date=2023-02-01")
    json_result = response.json()

    assert response.status_code == 200
    assert len(json_result) == 1


def test_consolidate_balance(client, db_session):
    add_portfolio(db_session)
    add_investments(db_session)
    add_consolidated_portfolio(db_session)

    response = client.post("/portfolios/PORT101/consolidations/consolidate")
    assert response.status_code == 200

    response = client.get("/portfolios/PORT101/consolidations")
    json_result = response.json()[0]

    assert json_result["amount_invested"] == 2500
    assert json_result["balance"] == 12900


