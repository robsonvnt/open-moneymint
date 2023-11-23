from finance.repository.db.prepare_to_db_test import *


def test_get_transactions(client, db_session):
    add_accounts(db_session)
    add_transactions(db_session)
    response = client.get(
        "/finances/transactions?account_code=ACC123&start_date=2023-05-01&end_date=2023-05-29"
    )
    json_result = response.json()

    assert response.status_code == 200
    assert len(json_result) == 2


def test_get_transactions_empty_dates(client, db_session):
    add_accounts(db_session)
    add_transactions(db_session)
    response = client.get(
        "/finances/transactions?account_code=ACC123"
    )
    json_result = response.json()

    assert response.status_code == 200
    assert len(json_result) == 3


def test_get_transactions_account_other_user(client, db_session):
    add_accounts(db_session)
    add_transactions(db_session)
    response = client.get(
        "/finances/transactions?account_code=ACC124"
    )

    assert response.status_code == 404


def test_get_transaction(client, db_session):
    add_accounts(db_session)
    add_transactions(db_session)
    response = client.get(
        "/finances/transactions/TRA001"
    )
    json_result = response.json()

    assert response.status_code == 200
    assert json_result["description"] == "Description 1"


def test_get_transaction_non_existent(client, db_session):
    add_accounts(db_session)
    add_transactions(db_session)
    response = client.get(
        "/finances/transactions/non_existent"
    )

    assert response.status_code == 404


def test_get_transaction_other_user(client, db_session):
    add_accounts(db_session)
    add_transactions(db_session)
    response = client.get(
        "/finances/transactions/TRA004"
    )

    assert response.status_code == 404
