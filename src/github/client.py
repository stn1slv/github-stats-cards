"""GitHub API client for making authenticated requests."""

from typing import Any, cast

import httpx

from ..core.constants import API_TIMEOUT, GRAPHQL_ENDPOINT
from ..core.exceptions import APIError


class GitHubClient:
    """Helper client for GitHub API interactions."""

    def __init__(self, token: str) -> None:
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        self.timeout = float(API_TIMEOUT)

    def graphql_query(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Execute a GraphQL query (synchronous).

        Args:
            query: GraphQL query string
            variables: Optional variables for the query

        Returns:
            JSON response data

        Raises:
            APIError: If API request fails
        """
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    GRAPHQL_ENDPOINT,
                    json={"query": query, "variables": variables or {}},
                    headers=self.headers,
                )
                response.raise_for_status()
                return cast(dict[str, Any], response.json())
        except httpx.HTTPError as e:
            raise APIError(f"GitHub API request failed: {e}") from e

    async def async_graphql_query(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Execute a GraphQL query (asynchronous).

        Args:
            query: GraphQL query string
            variables: Optional variables for the query

        Returns:
            JSON response data

        Raises:
            APIError: If API request fails
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    GRAPHQL_ENDPOINT,
                    json={"query": query, "variables": variables or {}},
                    headers=self.headers,
                )
                response.raise_for_status()
                return cast(dict[str, Any], response.json())
        except httpx.HTTPError as e:
            raise APIError(f"GitHub API request failed: {e}") from e

    def rest_get(self, url: str, headers: dict[str, str] | None = None) -> dict[str, Any]:
        """
        Execute a REST GET request (synchronous).

        Args:
            url: Full URL for the request
            headers: Optional additional headers

        Returns:
            JSON response data

        Raises:
            APIError: If API request fails
        """
        request_headers = self.headers.copy()
        if headers:
            request_headers.update(headers)

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    url,
                    headers=request_headers,
                )
                response.raise_for_status()
                return cast(dict[str, Any], response.json())
        except httpx.HTTPError as e:
            raise APIError(f"GitHub API request failed: {e}") from e

    def fetch_image(self, url: str) -> bytes | None:
        """
        Fetch an image from a URL (synchronous).

        Args:
            url: Image URL

        Returns:
            Image binary content or None if failed
        """
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url)
                response.raise_for_status()
                return cast(bytes, response.content)
        except httpx.HTTPError:
            return None

    async def async_fetch_image(self, url: str) -> bytes | None:
        """
        Fetch an image from a URL (asynchronous).

        Args:
            url: Image URL

        Returns:
            Image binary content or None if failed
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                response.raise_for_status()
                return cast(bytes, response.content)
        except httpx.HTTPError:
            return None
