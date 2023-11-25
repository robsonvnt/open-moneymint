from finance.domain.account_erros import AccountNotFound
from finance.repository.db.prepare_to_db_test import *


def test_get_all_accounts(client, db_session):
    add_accounts(db_session)

    response = client.get("/finances/accounts")
    json_result = response.json()

    assert response.status_code == 200
    assert isinstance(json_result, list)
    assert len(json_result) == 2


def test_get_account(client, db_session):
    add_accounts(db_session)

    response = client.get("/finances/accounts/ACC123")
    json_result = response.json()
    assert response.status_code == 200
    assert json_result["code"] == "ACC123"
    assert json_result["name"] == "Existing Account"


def test_get_non_existent_account(client, db_session):
    add_accounts(db_session)

    response = client.get("/finances/accounts/NONEXISTENT")
    assert response.status_code == 404


def test_post_account(client, db_session):
    add_accounts(db_session)

    new_account_data = {
        "name": "Existing Account",
        "description": "Description for ACC123"
    }

    response = client.post("/finances/accounts", json=new_account_data)
    json_result = response.json()

    assert response.status_code == 200
    assert len(json_result["code"]) == 10
    assert json_result["name"] == "Existing Account"
    assert json_result["user_code"] == "USER001"


def test_post_account_bad_request(client, db_session):
    add_accounts(db_session)
    response = client.post("/finances/accounts", json={})
    assert response.status_code == 422


def test_update_account(client, db_session):
    add_accounts(db_session)
    account_input = {
        "name": "Updated Account",
        "description": "Updated Description",
        "user_code": "USER001",
        "code": "ACC123"
    }

    response = client.put("/finances/accounts/ACC123", json=account_input)

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Account"


def test_update_account_not_found(client):
    mock_account_input = {
        "name": "Updated Account",
        "description": "Updated Description",
        "user_code": "USER001",
        "code": "ACC123"
    }
    response = client.put("/finances/accounts/NONEXISTENT", json=mock_account_input)

    assert response.status_code == 404


def test_delete_account(client, db_session):
    add_accounts(db_session)
    response = client.delete("/finances/accounts/ACC123")

    assert response.status_code == 200
    assert response.json()["message"] == "Account deleted successfully"


def test_delete_account_not_found(client, db_session):
    add_accounts(db_session)
    response = client.delete("/finances/accounts/NONEXISTENT")

    assert response.status_code == 404
