import json
import pytest
import requests_mock

from app import app_master


@pytest.fixture
def client():
    app_master.config["TESTING"] = True
    client = app_master.test_client()

    yield client


def test_index_route(client):
    response = client.get("/master/")
    assert response.status_code == 200
    assert response.data == b"This is the main page for Mater Server"


def test_app_master_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"This is Master Service"


def test_get_messages_route(client):
    response = client.get("/master/messages")

    assert response.status_code == 200
    data = json.loads(response.data.decode("utf-8"))
    assert data == []


def test_get_messages_route_non_empty(client):
    # Assuming you have a list of messages to add to in_memory_list
    messages = [{"message": "Message 1"}, {"message": "Message 2"}]

    for message in messages:
        client.post("/master/append", json=message)

    response = client.get("/master/messages")

    assert response.status_code == 200
    data = json.loads(response.data.decode("utf-8"))
    assert len(data) == len(messages)


def test_append_message_route(client):
    message = {"message": "Hello, World!"}

    with requests_mock.Mocker() as m:
        m.post(
            "http://localhost:5002/secondary1/replicate",
            json={"acknowledged": True},
            status_code=200,
        )
        m.post(
            "http://localhost:5003/secondary2/replicate",
            json={"acknowledged": True},
            status_code=200,
        )
        response = client.post("/master/append", json=message)

    assert response.status_code == 200
    assert response.data == b"Message replicated on all Secondaries"


def test_append_message_route_failed_replication_secondary1(client):
    message = {"message": "Hello, World!"}

    with requests_mock.Mocker() as m:
        m.post(
            "http://localhost:5002/secondary1/replicate",
            json={"acknowledged": False},
            status_code=200,
        )
        m.post(
            "http://localhost:5003/secondary2/replicate",
            json={"acknowledged": True},
            status_code=200,
        )
        response = client.post("/master/append", json=message)

    assert response.status_code == 200
    assert response.data == b"Failed to replicate message on all Secondaries"


def test_append_message_route_failed_replication_secondary2(client):
    message = {"message": "Hello, World!"}

    with requests_mock.Mocker() as m:
        m.post(
            "http://localhost:5002/secondary1/replicate",
            json={"acknowledged": True},
            status_code=200,
        )
        m.post(
            "http://localhost:5003/secondary2/replicate",
            json={"acknowledged": False},
            status_code=200,
        )
        response = client.post("/master/append", json=message)

    assert response.status_code == 200
    assert response.data == b"Failed to replicate message on all Secondaries"


def test_append_message_route_missing_message(client):
    response = client.post("/master/append", json={})

    assert response.status_code == 400
    data = json.loads(response.data.decode("utf-8"))
    assert data == {"error": "Message not provided"}
