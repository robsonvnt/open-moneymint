from datetime import timedelta

from finance.repository.db.prepare_to_db_test import *


def test_get_consolidations_start_month_end_month(client, db_session):
    add_account_consolidations(db_session)
    response = client.get(
        "/finances/consolidations?account_codes=ACC001&start_month=2023-08&end_month=2023-09"
    )
    json_result = response.json()

    assert response.status_code == 200
    assert len(json_result) == 2


def test_get_consolidations_month(client, db_session):
    add_account_consolidations(db_session)
    response = client.get(
        "/finances/consolidations?account_codes=ACC001&month=2023-08"
    )
    json_result = response.json()

    assert response.status_code == 200
    assert len(json_result) == 1
    assert json_result[0]["balance"] == 100

    response = client.get(
        "/finances/consolidations?account_codes=ACC001&month=2023-09"
    )
    json_result = response.json()
    assert response.status_code == 200
    assert len(json_result) == 1
    assert json_result[0]["balance"] == 110


def test_test_get_consolidations_last_month(client, db_session):
    preview_month = (date.today().replace(day=1) - timedelta(days=1)).replace(day=1)

    consolidations = [
        AccountConsolidation(account_code="ACC001", month=preview_month, balance=100),
        AccountConsolidation(account_code="ACC001", month=date(2023, 9, 1), balance=110),
        AccountConsolidation(account_code="ACC001", month=date(2023, 10, 1), balance=120)
    ]
    db_session.add_all(consolidations)
    db_session.commit()

    response = client.get(
        "/finances/consolidations/last-month?account_codes=ACC001"
    )
    json_result = response.json()

    assert response.status_code == 200
    assert json_result[0]["balance"] == 100


def test_get_current_month_consolidations(client, db_session):
    current_month = date.today().replace(day=1)

    consolidations = [
        AccountConsolidation(account_code="ACC001", month=current_month, balance=100),
        AccountConsolidation(account_code="ACC001", month=date(2023, 9, 1), balance=110),
        AccountConsolidation(account_code="ACC001", month=date(2023, 10, 1), balance=120)
    ]
    db_session.add_all(consolidations)
    db_session.commit()

    response = client.get(
        "/finances/consolidations/current-month?account_codes=ACC001"
    )
    json_result = response.json()

    assert response.status_code == 200
    assert json_result[0]["balance"] == 100


def test_get_sum_consolidations_grouped_by_category(client, db_session):
    current_month = date.today().replace(day=1)

    accounts = [
        Account(code="A1", name="Existing Account", description="Description for ACC123", user_code="USER001"),
        Account(code="A2", name="Second Account", description="Description for ACC124", user_code="USER001"),
        Account(code="A3", name="Other USER456's Account", description="Description for ACC125",
                user_code="USER001"),
    ]
    db_session.add_all(accounts)

    created_at = date.today()
    categories = [
        Category(code="C1", name="Cat Test 1", user_code="U1",
                 parent_category_code=None, created_at=created_at),
        Category(code="C2", name="Cat Test 2", user_code="U1",
                 parent_category_code=None, created_at=created_at),
        Category(code="C3", name="Cat Test 3", user_code="U1",
                 parent_category_code=None, created_at=created_at),
        Category(code="C21", name="Cat Test 2.1", user_code="U1",
                 parent_category_code="C2", created_at=created_at),
        Category(code="C22", name="Cat Test 2.2", user_code="U1",
                 parent_category_code="C2", created_at=created_at),
        Category(code="C211", name="Cat Test 2.1.1", user_code="U1",
                 parent_category_code="C21", created_at=created_at)
    ]
    db_session.add_all(categories)
    transactions = [
        FinancialTransaction(
            code="T1", account_code="A1", description="", category_code="C1",
            type=TransactionType.TRANSFER.value, date=date(2023, 8, 5), value=-50.0
        ),
        FinancialTransaction(
            code="T2", account_code="A1", description="", category_code="C1",
            type=TransactionType.TRANSFER.value, date=date(2023, 8, 5), value=-50.0
        ),

        FinancialTransaction(
            code="T3", account_code="A1", description="", category_code="C2",
            type=TransactionType.WITHDRAWAL.value, date=date(2023, 8, 10), value=-30
        ),
        FinancialTransaction(
            code="T4", account_code="A1", description="", category_code="C21",
            type=TransactionType.WITHDRAWAL.value, date=date(2023, 8, 5), value=-70
        ),
        FinancialTransaction(
            code="T5", account_code="A2", description="", category_code="C22",
            type=TransactionType.WITHDRAWAL.value, date=date(2023, 8, 5), value=-120
        ),
        FinancialTransaction(
            code="T6", account_code="A2", description="", category_code="C211",
            type=TransactionType.TRANSFER.value, date=date(2023, 8, 5), value=-50
        ),
        FinancialTransaction(
            code="T7", account_code="A2", description="", category_code="C211",
            type=TransactionType.WITHDRAWAL.value, date=date(2023, 8, 5), value=-30
        ),
        FinancialTransaction(
            code="T8", account_code="A2", description="", category_code="C211",
            type=TransactionType.DEPOSIT.value, date=date(2023, 8, 5), value=30
        ),
        FinancialTransaction(
            code="T9", account_code="A2", description="", category_code="C211",
            type=TransactionType.TRANSFER.value, date=date(2023, 9, 5), value=-30
        ),
        FinancialTransaction(
            code="T10", account_code="A3", description="", category_code="C3",
            type=TransactionType.TRANSFER.value, date=date(2023, 8, 5), value=-1000
        )
    ]
    db_session.add_all(transactions)
    db_session.commit()

    response = client.get(
        "/finances/consolidations/grouped-by-category?account_codes=A1&account_codes=A2&month=2023-08"
    )
    json_result = response.json()

    assert response.status_code == 200
    assert len(json_result) == 2
    assert json_result[0]["category"] == "Cat Test 1"
    assert json_result[0]["value"] == -100
    assert json_result[1]["category"] == "Cat Test 2"
    assert json_result[1]["value"] == -300
