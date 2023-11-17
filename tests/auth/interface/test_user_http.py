from datetime import date

import pytest

from src.auth.domain.models import UserModel
from src.auth.services import UserServiceFactory
from tests.auth.prepareto_db_test import db_session, client


@pytest.fixture
def user():
    return UserModel(name="User Test", code="123", user_name="user_name",
                     password="password", created_at=date.today())


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


def test_signin(monkeypatch, client, db_session, user):
    monkeypatch.setenv("SECRET_KEY", "secret_key")
    UserServiceFactory.create_user_service(db_session).create(user)

    login_data = {
        "user_name": "user_name",
        "password": "password"
    }

    response = client.post("/users/signin", json=login_data)
    json_result = response.json()

    assert response.status_code == 200
    assert "access_token" in json_result.keys()
    assert len(json_result["access_token"]) > 0


def test_signin_invalid_user_name(monkeypatch, client, db_session, user):
    monkeypatch.setenv("SECRET_KEY", "secret_key")
    UserServiceFactory.create_user_service(db_session).create(user)

    login_data = {
        "user_name": "invalid_user_name",
        "password": "password"
    }

    response = client.post("/users/signin", json=login_data)

    assert response.status_code == 400


def test_signin_invalid_password(monkeypatch, client, db_session, user):
    monkeypatch.setenv("SECRET_KEY", "secret_key")
    UserServiceFactory.create_user_service(db_session).create(user)

    login_data = {
        "user_name": "user_name",
        "password": "invalid_password"
    }

    response = client.post("/users/signin", json=login_data)

    assert response.status_code == 400


def test_get_me(client, monkeypatch, db_session, user):
    monkeypatch.setenv("SECRET_KEY", "secret_key")
    UserServiceFactory.create_user_service(db_session).create(user)
    login_data = {
        "user_name": "user_name",
        "password": "password"
    }
    signin_json_result = client.post("/users/signin", json=login_data).json()
    token_valido = signin_json_result["access_token"]

    response = client.get("/users/me", headers={"Authorization": f"Bearer {token_valido}"})
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["user_name"] == user.user_name
    assert len(response_json["code"]) == 10
