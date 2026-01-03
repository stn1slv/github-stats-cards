"""Tests for language fetcher utilities."""

from unittest.mock import Mock

import pytest

from src.langs_fetcher import (
    Language,
    LanguageFetchError,
    fetch_top_languages,
)


def test_language_dataclass():
    """Test Language dataclass creation."""
    lang = Language(name="Python", color="#3572A5", size=1000, count=5)
    assert lang.name == "Python"
    assert lang.color == "#3572A5"
    assert lang.size == 1000
    assert lang.count == 5


def test_fetch_top_languages_success(mocker):
    """Test successful language fetching."""
    mock_response_data = {
        "data": {
            "user": {
                "repositories": {
                    "nodes": [
                        {
                            "name": "repo1",
                            "languages": {
                                "edges": [
                                    {
                                        "size": 1000,
                                        "node": {"name": "Python", "color": "#3572A5"},
                                    },
                                    {
                                        "size": 500,
                                        "node": {"name": "JavaScript", "color": "#f1e05a"},
                                    },
                                ]
                            },
                        },
                        {
                            "name": "repo2",
                            "languages": {
                                "edges": [
                                    {
                                        "size": 800,
                                        "node": {"name": "Python", "color": "#3572A5"},
                                    },
                                ]
                            },
                        },
                    ]
                }
            }
        }
    }

    mock_response = Mock()
    mock_response.json.return_value = mock_response_data
    mock_response.raise_for_status.return_value = None

    mocker.patch("requests.post", return_value=mock_response)

    langs = fetch_top_languages("testuser", "test_token")

    assert "Python" in langs
    assert "JavaScript" in langs
    assert langs["Python"].size == 1800  # 1000 + 800
    assert langs["Python"].count == 2
    assert langs["JavaScript"].size == 500
    assert langs["JavaScript"].count == 1


def test_fetch_top_languages_exclude_repos(mocker):
    """Test excluding specific repositories."""
    mock_response_data = {
        "data": {
            "user": {
                "repositories": {
                    "nodes": [
                        {
                            "name": "repo1",
                            "languages": {
                                "edges": [
                                    {"size": 1000, "node": {"name": "Python", "color": "#3572A5"}}
                                ]
                            },
                        },
                        {
                            "name": "excluded-repo",
                            "languages": {
                                "edges": [
                                    {
                                        "size": 5000,
                                        "node": {"name": "JavaScript", "color": "#f1e05a"},
                                    }
                                ]
                            },
                        },
                    ]
                }
            }
        }
    }

    mock_response = Mock()
    mock_response.json.return_value = mock_response_data
    mock_response.raise_for_status.return_value = None

    mocker.patch("requests.post", return_value=mock_response)

    langs = fetch_top_languages("testuser", "test_token", exclude_repo=["excluded-repo"])

    assert "Python" in langs
    assert "JavaScript" not in langs


def test_fetch_top_languages_with_weights(mocker):
    """Test language ranking with custom weights."""
    mock_response_data = {
        "data": {
            "user": {
                "repositories": {
                    "nodes": [
                        {
                            "name": "repo1",
                            "languages": {
                                "edges": [
                                    {"size": 100, "node": {"name": "Python", "color": "#3572A5"}}
                                ]
                            },
                        },
                    ]
                }
            }
        }
    }

    mock_response = Mock()
    mock_response.json.return_value = mock_response_data
    mock_response.raise_for_status.return_value = None

    mocker.patch("requests.post", return_value=mock_response)

    # With size_weight=0.5, count_weight=0.5
    langs = fetch_top_languages("testuser", "test_token", size_weight=0.5, count_weight=0.5)

    assert "Python" in langs
    # size = (100 ** 0.5) * (1 ** 0.5) = 10
    assert langs["Python"].size == 10


def test_fetch_top_languages_api_error(mocker):
    """Test handling of GraphQL API errors."""
    mock_response_data = {"errors": [{"message": "User not found"}]}

    mock_response = Mock()
    mock_response.json.return_value = mock_response_data
    mock_response.raise_for_status.return_value = None

    mocker.patch("requests.post", return_value=mock_response)

    with pytest.raises(LanguageFetchError, match="User not found"):
        fetch_top_languages("nonexistent", "test_token")


def test_fetch_top_languages_network_error(mocker):
    """Test handling of network errors."""
    import requests

    mocker.patch("requests.post", side_effect=requests.RequestException("Network error"))

    with pytest.raises(LanguageFetchError, match="Failed to fetch data"):
        fetch_top_languages("testuser", "test_token")


def test_fetch_top_languages_no_data(mocker):
    """Test handling when no data is returned."""
    mock_response_data = {"data": None}

    mock_response = Mock()
    mock_response.json.return_value = mock_response_data
    mock_response.raise_for_status.return_value = None

    mocker.patch("requests.post", return_value=mock_response)

    with pytest.raises(LanguageFetchError, match="No data returned"):
        fetch_top_languages("testuser", "test_token")


def test_fetch_top_languages_user_not_found(mocker):
    """Test handling when user is not found."""
    mock_response_data = {"data": {"user": None}}

    mock_response = Mock()
    mock_response.json.return_value = mock_response_data
    mock_response.raise_for_status.return_value = None

    mocker.patch("requests.post", return_value=mock_response)

    with pytest.raises(LanguageFetchError, match="not found"):
        fetch_top_languages("nonexistent", "test_token")


def test_fetch_top_languages_missing_color(mocker):
    """Test handling languages with missing color."""
    mock_response_data = {
        "data": {
            "user": {
                "repositories": {
                    "nodes": [
                        {
                            "name": "repo1",
                            "languages": {
                                "edges": [
                                    {
                                        "size": 1000,
                                        "node": {"name": "CustomLang", "color": None},
                                    }
                                ]
                            },
                        },
                    ]
                }
            }
        }
    }

    mock_response = Mock()
    mock_response.json.return_value = mock_response_data
    mock_response.raise_for_status.return_value = None

    mocker.patch("requests.post", return_value=mock_response)

    langs = fetch_top_languages("testuser", "test_token")

    assert "CustomLang" in langs
    assert langs["CustomLang"].color == "#858585"  # Default color
