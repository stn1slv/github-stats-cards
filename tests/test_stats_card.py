"""Tests for stats card renderer."""

from src.config import StatsCardConfig
from src.stats_card import render_stats_card
from src.fetcher import UserStats


def test_render_stats_card_basic():
    """Test basic stats card rendering."""
    stats: UserStats = {
        "name": "Test User",
        "login": "testuser",
        "totalCommits": 1000,
        "totalPRs": 100,
        "mergedPRs": 90,
        "totalIssues": 50,
        "totalStars": 200,
        "contributedTo": 25,
        "followers": 50,
        "totalReviews": 10,
        "discussionsStarted": 5,
        "discussionsAnswered": 8,
    }

    config = StatsCardConfig()
    svg = render_stats_card(stats, config)

    # Check that SVG contains expected elements
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "Test User" in svg or "testuser" in svg
    assert "Total Stars" in svg
    assert "Total Commits" in svg


def test_render_stats_card_hide_stats():
    """Test hiding specific stats."""
    stats: UserStats = {
        "name": "Test User",
        "login": "testuser",
        "totalCommits": 1000,
        "totalPRs": 100,
        "mergedPRs": 90,
        "totalIssues": 50,
        "totalStars": 200,
        "contributedTo": 25,
        "followers": 50,
        "totalReviews": 10,
        "discussionsStarted": 5,
        "discussionsAnswered": 8,
    }

    config = StatsCardConfig(hide=["stars", "prs"])

    svg = render_stats_card(stats, config)

    assert "Total Stars" not in svg
    assert "Total PRs" not in svg
    assert "Total Commits" in svg


def test_render_stats_card_show_additional():
    """Test showing additional stats."""
    stats: UserStats = {
        "name": "Test User",
        "login": "testuser",
        "totalCommits": 1000,
        "totalPRs": 100,
        "mergedPRs": 90,
        "totalIssues": 50,
        "totalStars": 200,
        "contributedTo": 25,
        "followers": 50,
        "totalReviews": 10,
        "discussionsStarted": 5,
        "discussionsAnswered": 8,
    }

    config = StatsCardConfig(show=["reviews", "discussions_started"])
    svg = render_stats_card(stats, config)

    assert "Total Reviews" in svg
    assert "Discussions Started" in svg


def test_render_stats_card_custom_theme():
    """Test custom theme."""
    stats: UserStats = {
        "name": "Test User",
        "login": "testuser",
        "totalCommits": 1000,
        "totalPRs": 100,
        "mergedPRs": 90,
        "totalIssues": 50,
        "totalStars": 200,
        "contributedTo": 25,
        "followers": 50,
        "totalReviews": 10,
        "discussionsStarted": 5,
        "discussionsAnswered": 8,
    }

    config = StatsCardConfig(theme="dark")
    svg = render_stats_card(stats, config)

    assert "<svg" in svg
    # Dark theme colors should be applied
    assert "#fff" in svg or "#9f9f9f" in svg


def test_render_stats_card_hide_rank():
    """Test hiding rank circle."""
    stats: UserStats = {
        "name": "Test User",
        "login": "testuser",
        "totalCommits": 1000,
        "totalPRs": 100,
        "mergedPRs": 90,
        "totalIssues": 50,
        "totalStars": 200,
        "contributedTo": 25,
        "followers": 50,
        "totalReviews": 10,
        "discussionsStarted": 5,
        "discussionsAnswered": 8,
    }

    config_with_rank = StatsCardConfig(hide_rank=False)
    config_without_rank = StatsCardConfig(hide_rank=True)
    svg_with_rank = render_stats_card(stats, config_with_rank)
    svg_without_rank = render_stats_card(stats, config_without_rank)

    # Check for actual rank circle element, not just CSS classes
    assert 'data-testid="rank-circle"' in svg_with_rank
    assert 'data-testid="rank-circle"' not in svg_without_rank


def test_render_stats_card_custom_title():
    """Test custom title."""
    stats: UserStats = {
        "name": "Test User",
        "login": "testuser",
        "totalCommits": 1000,
        "totalPRs": 100,
        "mergedPRs": 90,
        "totalIssues": 50,
        "totalStars": 200,
        "contributedTo": 25,
        "followers": 50,
        "totalReviews": 10,
        "discussionsStarted": 5,
        "discussionsAnswered": 8,
    }

    config = StatsCardConfig(custom_title="My Custom Stats")
    svg = render_stats_card(stats, config)

    assert "My Custom Stats" in svg
