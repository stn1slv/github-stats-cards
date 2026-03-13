"""Tests for GitHub language data fetching."""

from unittest.mock import patch

import pytest

from src.core.config import LangsFetchConfig
from src.core.exceptions import APIError
from src.github.langs_fetcher import Language, LanguageFetchError, fetch_top_languages


def test_language_dataclass():
    lang = Language(name="Python", color="#3572A5", size=1000, count=2)
    assert lang.name == "Python"
    assert lang.color == "#3572A5"
    assert lang.size == 1000
    assert lang.count == 2
    assert lang.score == 0  # default before weighting


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _make_repos_response(nodes: list[dict], has_next_page: bool = False, end_cursor: str | None = None) -> dict:
    """Build a minimal GraphQL response containing repository nodes."""
    return {
        "data": {
            "user": {
                "repositories": {
                    "nodes": nodes,
                    "pageInfo": {
                        "hasNextPage": has_next_page,
                        "endCursor": end_cursor,
                    },
                }
            }
        }
    }


_REPO_PYTHON_JS = [
    {
        "name": "repo1",
        "languages": {
            "edges": [
                {"size": 100, "node": {"name": "Python", "color": "#3572A5"}},
                {"size": 50, "node": {"name": "JavaScript", "color": "#f1e05a"}},
            ]
        },
    }
]


# ---------------------------------------------------------------------------
# Success paths
# ---------------------------------------------------------------------------


@patch("src.github.langs_fetcher.GitHubClient")
def test_fetch_top_languages_success(MockClient):
    MockClient.return_value.__enter__.return_value = MockClient.return_value
    MockClient.return_value.__exit__.return_value = False
    MockClient.return_value.graphql_query.return_value = _make_repos_response(_REPO_PYTHON_JS)

    config = LangsFetchConfig(username="testuser", token="testtoken")
    result = fetch_top_languages(config)

    assert len(result) == 2
    assert "Python" in result
    assert result["Python"].size == 100
    assert result["Python"].score == 100  # default weights: score == size
    assert result["JavaScript"].size == 50
    assert result["Python"].color == "#3572A5"


@patch("src.github.langs_fetcher.GitHubClient")
def test_fetch_top_languages_exclude_repos(MockClient):
    MockClient.return_value.__enter__.return_value = MockClient.return_value
    MockClient.return_value.__exit__.return_value = False
    nodes = [
        {
            "name": "repo1",
            "languages": {"edges": [{"size": 100, "node": {"name": "Python"}}]},
        },
        {
            "name": "repo2",
            "languages": {"edges": [{"size": 200, "node": {"name": "JavaScript"}}]},
        },
    ]
    MockClient.return_value.graphql_query.return_value = _make_repos_response(nodes)

    config = LangsFetchConfig(username="testuser", token="testtoken", exclude_repo=["repo2"])
    result = fetch_top_languages(config)

    assert len(result) == 1
    assert "Python" in result
    assert "JavaScript" not in result


@patch("src.github.langs_fetcher.GitHubClient")
def test_fetch_top_languages_with_weights(MockClient):
    MockClient.return_value.__enter__.return_value = MockClient.return_value
    MockClient.return_value.__exit__.return_value = False
    nodes = [
        {"name": "repo1", "languages": {"edges": [{"size": 100, "node": {"name": "Python"}}]}},
        {"name": "repo2", "languages": {"edges": [{"size": 100, "node": {"name": "Python"}}]}},
    ]
    MockClient.return_value.graphql_query.return_value = _make_repos_response(nodes)

    # size^0.5 * count^1.0 = (200^0.5) * (2^1.0) = 14.14 * 2 = 28.28 -> 28
    config = LangsFetchConfig(username="testuser", token="testtoken", size_weight=0.5, count_weight=1.0)
    result = fetch_top_languages(config)

    assert result["Python"].score == 28
    assert result["Python"].size == 200  # original bytes preserved


@patch("src.github.langs_fetcher.GitHubClient")
def test_fetch_top_languages_missing_color(MockClient):
    MockClient.return_value.__enter__.return_value = MockClient.return_value
    MockClient.return_value.__exit__.return_value = False
    nodes = [
        {
            "name": "repo1",
            "languages": {"edges": [{"size": 100, "node": {"name": "Python", "color": None}}]},
        }
    ]
    MockClient.return_value.graphql_query.return_value = _make_repos_response(nodes)

    config = LangsFetchConfig(username="testuser", token="testtoken")
    result = fetch_top_languages(config)
    assert result["Python"].color == "#858585"  # Default color


# ---------------------------------------------------------------------------
# Error paths
# ---------------------------------------------------------------------------


@patch("src.github.langs_fetcher.GitHubClient")
def test_fetch_top_languages_api_error(MockClient):
    MockClient.return_value.__enter__.return_value = MockClient.return_value
    MockClient.return_value.__exit__.return_value = False
    MockClient.return_value.graphql_query.side_effect = APIError("Not Found")

    config = LangsFetchConfig(username="testuser", token="testtoken")
    with pytest.raises(LanguageFetchError, match="Failed to fetch data"):
        fetch_top_languages(config)


@patch("src.github.langs_fetcher.GitHubClient")
def test_fetch_top_languages_no_data(MockClient):
    MockClient.return_value.__enter__.return_value = MockClient.return_value
    MockClient.return_value.__exit__.return_value = False
    MockClient.return_value.graphql_query.return_value = {"data": None}

    config = LangsFetchConfig(username="testuser", token="testtoken")
    with pytest.raises(LanguageFetchError, match="No data returned"):
        fetch_top_languages(config)


@patch("src.github.langs_fetcher.GitHubClient")
def test_fetch_top_languages_user_not_found(MockClient):
    MockClient.return_value.__enter__.return_value = MockClient.return_value
    MockClient.return_value.__exit__.return_value = False
    MockClient.return_value.graphql_query.return_value = {"data": {"user": None}}

    config = LangsFetchConfig(username="testuser", token="testtoken")
    with pytest.raises(LanguageFetchError, match="User 'testuser' not found"):
        fetch_top_languages(config)


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------


@patch("src.github.langs_fetcher.GitHubClient")
def test_fetch_top_languages_pagination(MockClient):
    """Test that repositories across multiple pages are aggregated."""
    MockClient.return_value.__enter__.return_value = MockClient.return_value
    MockClient.return_value.__exit__.return_value = False

    page1 = _make_repos_response(
        [{"name": "repo1", "languages": {"edges": [{"size": 100, "node": {"name": "Python", "color": "#3572A5"}}]}}],
        has_next_page=True,
        end_cursor="cursor1",
    )
    page2 = _make_repos_response(
        [{"name": "repo2", "languages": {"edges": [{"size": 200, "node": {"name": "Python", "color": "#3572A5"}}]}}],
        has_next_page=False,
    )
    MockClient.return_value.graphql_query.side_effect = [page1, page2]

    config = LangsFetchConfig(username="testuser", token="testtoken")
    result = fetch_top_languages(config)

    assert result["Python"].size == 300
    assert result["Python"].count == 2
    assert MockClient.return_value.graphql_query.call_count == 2
