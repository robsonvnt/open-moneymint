from sqlalchemy.exc import NoResultFound

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


def test_get_categories_list(client, db_session):
    add_categories(db_session)
    response = client.get("/finances/categories/list")
    json_result = response.json()

    assert response.status_code == 200
    assert len(json_result) == 11
    for item in json_result:
        assert len(item["children"]) == 0


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

    assert response.status_code == 404


def test_get_categories_by_code_wrong_user(client, db_session):
    add_categories(db_session)
    response = client.get("/finances/categories/CAT0012")

    assert response.status_code == 404


def test_create_category(client, db_session):
    category_data = {
        "name": "Test name",
        "parent_category_code": None
    }
    response = client.post("/finances/categories", json=category_data)
    response_json = response.json()

    category = db_session.query(Category).filter(
        Category.user_code == "USER001"
    ).one()

    assert response.status_code == 200
    assert category.name == response_json["name"]


def test_create_category_bad_request(client):
    response = client.post("/finances/categories", json={"parent_category_code": None})
    assert response.status_code == 422


def test_update_category(client, db_session):
    add_categories(db_session)
    category_data = {
        "name": "Updated name",
        "parent_category_code": None,
    }
    response = client.put("/finances/categories/CAT001", json=category_data)
    response_json = response.json()

    category = db_session.query(Category).filter(
        Category.code == "CAT001"
    ).one()

    assert response.status_code == 200
    assert category.name == response_json["name"]
    assert category.name == category_data["name"]


def test_update_non_existent_category(client, db_session):
    add_categories(db_session)
    category_data = {
        "name": "Updated name",
        "parent_category_code": None,
    }
    response = client.put("/finances/categories/non_existent", json=category_data)

    assert response.status_code == 404


def test_update_category_of_other_user(client, db_session):
    add_categories(db_session)
    category_data = {
        "name": "Updated name",
        "parent_category_code": None,
    }
    response = client.put("/finances/categories/CAT0012", json=category_data)

    assert response.status_code == 404


def test_update_category_bad_request(client, db_session):
    add_categories(db_session)
    category_data = {
        "parent_category_code": None,
    }
    response = client.put("/finances/categories/CAT0012", json=category_data)

    assert response.status_code == 422


def test_delete_category(client, db_session):
    add_categories(db_session)

    response = client.delete("/finances/categories/CAT001")

    with pytest.raises(NoResultFound):
        db_session.query(Category).filter(
            Category.code == "CAT001"
        ).one()

    assert response.status_code == 200


def test_delete_non_existent_category(client, db_session):
    response = client.delete("/finances/categories/non_existent")
    assert response.status_code == 404


def test_delete_category_of_other_user(client, db_session):
    add_categories(db_session)
    response = client.delete("/finances/categories/CAT0012")

    assert response.status_code == 404
