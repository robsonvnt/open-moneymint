from finance.repository.db.prepare_to_db_test import *


def test_get_categories(client, db_session):
    add_categories(db_session)
    response = client.get("/finances/categories")
    json_result = response.json()

    assert response.status_code == 200
    assert len(json_result) == 4
    assert json_result[0]["code"] == "CAT001"
    assert len(json_result[0]["children"]) == 3
    assert len(json_result[0]["children"][1]["children"]) == 4


def test_get_categories_by_code(client, db_session):
    add_categories(db_session)
    response = client.get("/finances/categories/CAT001")
    json_result = response.json()

    assert response.status_code == 200
    assert json_result["code"] == "CAT001"
    assert json_result["name"] == "Main Category"
    assert json_result["parent_category_code"] is None
    assert json_result["created_at"] == str(date.today())


def test_get_categories_by_non_existent_code(client, db_session):
    add_categories(db_session)
    response = client.get("/finances/categories/non_existent")
    response.json()

    assert response.status_code == 404


def test_get_categories_by_code_wrong_user(client, db_session):
    add_categories(db_session)
    response = client.get("/finances/categories/CAT0012")
    response.json()

    assert response.status_code == 404
