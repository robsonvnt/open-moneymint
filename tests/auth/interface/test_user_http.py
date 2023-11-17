from tests.auth.prepareto_db_test import db_session, client


def test_signup_user(client):
    new_user_data = {
        "name": "test",
        "user_name": "test",
        "password": "test"
    }

    response = client.post("/users/signup", json=new_user_data)
    json_result = response.json()

    assert response.status_code == 200
    assert "code" in json_result.keys()
    assert len(json_result["code"]) == 10
    assert "password" not in json_result.keys()
