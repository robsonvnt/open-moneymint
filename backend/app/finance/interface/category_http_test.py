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
