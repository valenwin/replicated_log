import pytest
import json

from app import app_secondary1


@pytest.fixture
def client():
    app_secondary1.config["TESTING"] = True
    client = app_secondary1.test_client()

    yield client


def test_index_route(client):
    response = client.get("/secondary1/")
    assert response.status_code == 200
    assert response.data == b"This is the main page for Secondary Server"


def test_app_secondary1_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"This is Secondary1 Service"


def test_replicate_message(client):
    message = {"message": "Hello, World!", "id": "unique_id"}

    response = client.post("/secondary1/replicate", json=message)

    assert response.status_code == 200

    # Check if the response contains JSON with the "acknowledged" field set to True
    data = json.loads(response.data)
    assert data.get("acknowledged") is True


def test_replicate_message_empty_json(client):
    response = client.post("/secondary1/replicate", json={})

    assert response.status_code == 400


def test_get_acknowledged_messages(client):
    response = client.get("/secondary1/messages")
    assert response.status_code == 200

    try:
        data = json.loads(response.data)
        assert isinstance(data, list)
    except json.JSONDecodeError:
        assert False, "Response data is not valid JSON"
