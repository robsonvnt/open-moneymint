from finance.repository.db.prepare_to_db_test import *


def test_get_consolidations(client, db_session):
    add_account_consolidations(db_session)
    response = client.get(
        "/finances/consolidations?account_code=ACC001&start_month=2023-08&end_month=2023-09"
    )
    json_result = response.json()

    assert response.status_code == 200
    assert len(json_result) == 2
