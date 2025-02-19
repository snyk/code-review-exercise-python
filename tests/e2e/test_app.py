from http import HTTPStatus

from fastapi.testclient import TestClient

from app import app


def test_healthcheck():
    client = TestClient(app)
    response = client.get("/healthcheck")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_get_package_by_name_and_version():
    client = TestClient(app)
    response = client.get("/package/react/16.3.0")
    assert response.status_code == HTTPStatus.OK
    assert response.json().get("name") == "react"
    assert response.json().get("version") == "16.3.0"
    assert response.json().get("dependencies") is not None


def test_get_package_by_name():
    client = TestClient(app)
    response = client.get("/package/react")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() is not None


def test_unsupported_route():
    client = TestClient(app)
    response = client.get("/something")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() is not None
