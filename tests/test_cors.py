from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)
ALLOWED_ORIGIN = "http://127.0.0.1:5173"


def preflight(path: str):
    return client.options(
        path,
        headers={
            "Origin": ALLOWED_ORIGIN,
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "content-type",
        },
    )


def test_health_preflight_succeeds_with_cors_headers():
    response = preflight("/health")

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == ALLOWED_ORIGIN
    assert "GET" in response.headers["access-control-allow-methods"]
    assert "content-type" in response.headers["access-control-allow-headers"].lower()


def test_employees_preflight_succeeds_with_cors_headers():
    response = preflight("/employees")

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == ALLOWED_ORIGIN
    assert "GET" in response.headers["access-control-allow-methods"]
