import pytest
import json

from secondary2.app_secondary2 import app_secondary2


@pytest.fixture
def client():
    app_secondary2.config["TESTING"] = True
    client = app_secondary2.test_client()

    yield client


def test_index_route(client):
    response = client.get("/secondary2/")
    assert response.status_code == 200
    assert response.data == b"This is the main page for Secondary Server"


def test_app_secondary1_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"This is Secondary2 Service"


def test_replicate_message(client):
    message = {"message": "Hello, World!", "id": "unique_id"}

    response = client.post("/secondary2/replicate", json=message)

    assert response.status_code == 200

    # Check if the response contains JSON with the "acknowledged" field set to True
    data = json.loads(response.data)
    assert data.get("acknowledged") is True


def test_replicate_message_empty_json(client):
    response = client.post("/secondary2/replicate", json={})

    assert response.status_code == 400


def test_get_acknowledged_messages(client):
    response = client.get("/secondary2/messages")
    assert response.status_code == 200

    try:
        data = json.loads(response.data)
        assert isinstance(data, list)
    except json.JSONDecodeError:
        assert False, "Response data is not valid JSON"
