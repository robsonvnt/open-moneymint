from datetime import timedelta

from finance.repository.db.prepare_to_db_test import *


def test_get_consolidations(client, db_session):
    add_account_consolidations(db_session)
    response = client.get(
        "/finances/consolidations?account_code=ACC001&start_month=2023-08&end_month=2023-09"
    )
    json_result = response.json()

    assert response.status_code == 200
    assert len(json_result) == 2


def test_get_consolidations_last_month(client, db_session):
    preview_month = (date.today().replace(day=1) - timedelta(days=1)).replace(day=1)

    consolidations = [
        AccountConsolidation(account_code="ACC001", month=preview_month, balance=100),
        AccountConsolidation(account_code="ACC001", month=date(2023, 9, 1), balance=110),
        AccountConsolidation(account_code="ACC001", month=date(2023, 10, 1), balance=120)
    ]
    db_session.add_all(consolidations)
    db_session.commit()

    response = client.get(
        "/finances/consolidations/last-month?account_code=ACC001"
    )
    json_result = response.json()

    assert response.status_code == 200
    assert json_result["balance"] == 100


def get_current_month_consolidations(client, db_session):
    current_month = date.today().replace(day=1)

    consolidations = [
        AccountConsolidation(account_code="ACC001", month=current_month, balance=100),
        AccountConsolidation(account_code="ACC001", month=date(2023, 9, 1), balance=110),
        AccountConsolidation(account_code="ACC001", month=date(2023, 10, 1), balance=120)
    ]
    db_session.add_all(consolidations)
    db_session.commit()

    response = client.get(
        "/finances/consolidations/current-month?account_code=ACC001"
    )
    json_result = response.json()

    assert response.status_code == 200
    assert json_result["balance"] == 100
