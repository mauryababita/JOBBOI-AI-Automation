from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_and_login():
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Alice User",
            "email": "alice@example.com",
            "password": "securepassword",
            "phone": "+123456789",
            "location": "Bengaluru",
        },
    )
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["success"] is True
    token = payload["data"]["token"]

    login_response = client.post(
        "/api/auth/login",
        json={"email": "alice@example.com", "password": "securepassword"},
    )
    assert login_response.status_code == 200, login_response.text
    assert login_response.json()["data"]["token"]
