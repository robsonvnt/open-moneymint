from investment.repository.prepareto_db_test import *


def test_get_all_portfolios(client, db_session):
    # Adding sample portfolios to db_session as needed
    add_portfolio(db_session)

    response = client.get("/portfolios")
    json_result = response.json()

    assert response.status_code == 200
    assert isinstance(json_result, list)
    assert len(json_result) == 2


def test_get_portfolio(client, db_session):
    add_portfolio(db_session)  # Creating a sample portfolio

    response = client.get("/portfolios/PORT100")
    json_result = response.json()

    assert response.status_code == 200
    assert json_result["code"] == "PORT100"
    assert json_result["name"] == "Portfolio Name 100"

    # Test for non-existing portfolio
    response = client.get("/portfolios/NON_EXISTENT")
    assert response.status_code == 404


def test_create_portfolio(client, db_session):
    new_portfolio_data = {
        "name": "New Portfolio",
        "description": "A test portfolio"
    }
    response = client.post("/portfolios", json=new_portfolio_data)

    assert response.status_code == 200
    json_result = response.json()
    assert json_result["name"] == "New Portfolio"
    assert json_result["description"] == "A test portfolio"


def test_update_portfolio(client, db_session):
    add_portfolio(db_session)  # Creating a sample portfolio

    updated_data = {
        "code": "PORT100",
        "name": "Updated Portfolio",
        "description": "Updated Description",
        "user_code": "001"
    }
    response = client.put("/portfolios/PORT100", json=updated_data)

    assert response.status_code == 200
    json_result = response.json()
    assert json_result["name"] == "Updated Portfolio"

    # Test for non-existing portfolio update
    response = client.put("/portfolios/NON_EXISTENT", json=updated_data)
    assert response.status_code == 404


def test_delete_portfolio(client, db_session):
    add_portfolio(db_session)  # Creating a sample portfolio

    response = client.delete("/portfolios/PORT100")
    assert response.status_code == 200

    response = client.get("/portfolios/PORT100")
    assert response.status_code == 404

    # Test for deleting a non-existing portfolio
    response = client.delete("/portfolios/NON_EXISTENT")
    assert response.status_code == 404
