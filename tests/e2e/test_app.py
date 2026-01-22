from http import HTTPStatus

from fastapi.testclient import TestClient

from app import app


def test_healthcheck():
    client = TestClient(app)
    response = client.get("/healthcheck")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_get_package():
    client = TestClient(app)
    response = client.get("/package/minimatch/3.1.2")
    assert response.status_code == HTTPStatus.OK
    assert response.json().get("name") == "minimatch"
    assert response.json().get("version") == "3.1.2"
    assert response.json().get("dependencies") == [
        {
            "name": "brace-expansion",
            "version": "1.1.11",
            "dependencies": [
                {"name": "balanced-match", "version": "1.0.2", "dependencies": []},
                {"name": "concat-map", "version": "0.0.1", "dependencies": []},
            ],
        }
    ]


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
