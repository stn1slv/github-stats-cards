"""Tests for GitHub API client."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from src.core.exceptions import APIError
from src.github.client import GitHubClient


@pytest.fixture
def client():
    return GitHubClient(token="fake-token")


def test_client_init(client):
    assert client.token == "fake-token"
    assert client.headers["Authorization"] == "Bearer fake-token"
    assert client.headers["Content-Type"] == "application/json"


def test_graphql_query_success(client):
    with patch("httpx.Client.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": {"user": "test"}}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = client.graphql_query("query", {"var": "val"})

        assert result == {"data": {"user": "test"}}
        mock_post.assert_called_once()


def test_graphql_query_error(client):
    with patch("httpx.Client.post") as mock_post:
        mock_post.side_effect = httpx.HTTPError("Network error")

        with pytest.raises(APIError, match="GitHub API request failed"):
            client.graphql_query("query")


@pytest.mark.anyio
async def test_async_graphql_query_success(client):
    with patch("httpx.AsyncClient.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": {"user": "test"}}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = await client.async_graphql_query("query", {"var": "val"})

        assert result == {"data": {"user": "test"}}
        mock_post.assert_called_once()


@pytest.mark.anyio
async def test_async_graphql_query_error(client):
    with patch("httpx.AsyncClient.post") as mock_post:
        mock_post.side_effect = httpx.HTTPError("Network error")

        with pytest.raises(APIError, match="GitHub API request failed"):
            await client.async_graphql_query("query")


def test_rest_get_success(client):
    with patch("httpx.Client.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 123}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = client.rest_get("https://api.github.com/user")

        assert result == {"id": 123}
        mock_get.assert_called_once()


def test_rest_get_error(client):
    with patch("httpx.Client.get") as mock_get:
        mock_get.side_effect = httpx.HTTPError("Network error")

        with pytest.raises(APIError, match="GitHub API request failed"):
            client.rest_get("https://api.github.com/user")


def test_fetch_image_success(client):
    with patch("httpx.Client.get") as mock_get:
        mock_response = MagicMock()
        mock_response.content = b"image-data"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = client.fetch_image("https://example.com/image.png")

        assert result == b"image-data"


def test_fetch_image_error(client):
    with patch("httpx.Client.get") as mock_get:
        mock_get.side_effect = httpx.HTTPError("Network error")

        result = client.fetch_image("https://example.com/image.png")

        assert result is None


@pytest.mark.anyio
async def test_async_fetch_image_success(client):
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_response = MagicMock()
        mock_response.content = b"image-data"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = await client.async_fetch_image("https://example.com/image.png")

        assert result == b"image-data"


@pytest.mark.anyio
async def test_async_fetch_image_error(client):
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.side_effect = httpx.HTTPError("Network error")

        result = await client.async_fetch_image("https://example.com/image.png")

        assert result is None
