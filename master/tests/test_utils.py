import pytest
import requests
from unittest.mock import patch, MagicMock

from master.utils import replicate_to_secondaries


@pytest.mark.asyncio
async def test_successful_replication():
    # Mock the behavior of requests.post for a successful replication
    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"acknowledged": True}
        mock_post.return_value = mock_response

        message = {"data": "example data"}
        message_id = "example_message_id"

        result = await replicate_to_secondaries(message, message_id)

        assert result == "Message replicated on all Secondaries"
        mock_post.assert_called()


@pytest.mark.asyncio
async def test_failed_replication():
    # Mock the behavior of requests.post for a failed replication
    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 500  # Simulate a failure status code
        mock_response.json.return_value = {"acknowledged": False}
        mock_post.return_value = mock_response

        message = {"data": "example data"}
        message_id = "example_message_id"

        result = await replicate_to_secondaries(message, message_id)

        assert result == "Failed to replicate message on all Secondaries"
        mock_post.assert_called()


@pytest.mark.asyncio
async def test_request_exception_handling():
    # Mock requests.post to raise a RequestException
    with patch("requests.post", side_effect=requests.exceptions.RequestException):
        message = {"data": "example data"}
        message_id = "example_message_id"

        result = await replicate_to_secondaries(message, message_id)

        assert result == "Failed to replicate message on all Secondaries"
