"""GitHub API client for making authenticated requests."""

from typing import Any, cast

import requests  # type: ignore

from ..core.constants import API_TIMEOUT, GRAPHQL_ENDPOINT
from ..core.exceptions import APIError


class GitHubClient:
    """Helper client for GitHub API interactions."""

    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def graphql_query(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Execute a GraphQL query.

        Args:
            query: GraphQL query string
            variables: Optional variables for the query

        Returns:
            JSON response data

        Raises:
            APIError: If API request fails
        """
        try:
            response = requests.post(
                GRAPHQL_ENDPOINT,
                json={"query": query, "variables": variables or {}},
                headers=self.headers,
                timeout=API_TIMEOUT,
            )
            response.raise_for_status()
            return cast(dict[str, Any], response.json())
        except requests.exceptions.RequestException as e:
            raise APIError(f"GitHub API request failed: {e}") from e

    def rest_get(self, url: str, headers: dict[str, str] | None = None) -> dict[str, Any]:
        """
        Execute a REST GET request.

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
            response = requests.get(
                url,
                headers=request_headers,
                timeout=API_TIMEOUT,
            )
            response.raise_for_status()
            return cast(dict[str, Any], response.json())
        except requests.exceptions.RequestException as e:
            raise APIError(f"GitHub API request failed: {e}") from e

    def fetch_image(self, url: str) -> bytes | None:
        """
        Fetch an image from a URL.

        Args:
            url: Image URL

        Returns:
            Image binary content or None if failed
        """
        try:
            response = requests.get(
                url,
                timeout=API_TIMEOUT,
            )
            response.raise_for_status()
            return cast(bytes, response.content)
        except requests.exceptions.RequestException:
            return None
