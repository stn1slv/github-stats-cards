"""Tests for rank calculation algorithm."""

import pytest

from src.github.rank import (
    calculate_user_rank,
    calculate_repo_rank,
    exponential_cdf,
    log_normal_cdf,
)


# ---------------------------------------------------------------------------
# CDF helpers
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("x,expected", [(0, 0), (1, 0.5), (2, 0.75)])
def test_exponential_cdf(x, expected):
    assert exponential_cdf(x) == expected


@pytest.mark.parametrize("x,expected", [(0, 0), (1, 0.5), (9, 0.9)])
def test_log_normal_cdf(x, expected):
    assert log_normal_cdf(x) == expected


# ---------------------------------------------------------------------------
# calculate_user_rank
# ---------------------------------------------------------------------------
def test_calculate_user_rank_s_tier():
    result = calculate_user_rank(100000, 10000, 10000, 10000, 100000, 10000)
    assert result["level"] == "S"
    assert result["percentile"] <= 1.0


def test_calculate_user_rank_a_tier():
    result = calculate_user_rank(1000, 100, 50, 20, 100, 50)
    assert result["level"] in ["S", "A+", "A"]


def test_calculate_user_rank_c_tier():
    result = calculate_user_rank(10, 1, 1, 0, 0, 0)
    assert result["level"] in ["C+", "C"]


def test_calculate_user_rank_with_all_commits():
    res1 = calculate_user_rank(1000, 50, 25, 2, 50, 10, all_commits=False)
    res2 = calculate_user_rank(1000, 50, 25, 2, 50, 10, all_commits=True)
    assert res2["percentile"] > res1["percentile"]


def test_user_rank_percentile_range():
    res_best = calculate_user_rank(1000000, 100000, 100000, 10000, 100000, 100000)
    res_worst = calculate_user_rank(0, 0, 0, 0, 0, 0)
    assert 0 <= res_best["percentile"] <= 100
    assert 0 <= res_worst["percentile"] <= 100
    assert res_best["percentile"] < res_worst["percentile"]


# ---------------------------------------------------------------------------
# calculate_repo_rank
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "stars,commits,expected",
    [
        # S tier (>10000 stars)
        (10001, 5001, "S+"),
        (10001, 1000, "S"),
        (10001, 50, "S-"),
        # Boundary: 10000 stars → A tier
        (10000, 6000, "A+"),
        # A tier (>1000 stars)
        (1001, 6000, "A+"),
        (1001, 200, "A"),
        (1001, 10, "A-"),
        # Boundary: 1000 stars → B tier
        (1000, 6000, "B+"),
        # B tier (>100 stars)
        (101, 6000, "B+"),
        # Boundary: 100 stars → C tier
        (100, 6000, "C+"),
        # C tier (>10 stars)
        (11, 6000, "C+"),
        # Boundary: 10 stars → D tier
        (10, 6000, "D+"),
        # D tier (0-10 stars)
        (1, 6000, "D+"),
        (0, 6000, "D+"),
        # Commit modifier boundaries
        (10001, 5000, "S"),  # 5000 = neutral upper boundary
        (10001, 100, "S"),  # 100 = neutral lower boundary
        # 0 commits: neutral (no modifier)
        (10001, 0, "S"),
    ],
)
def test_calculate_repo_rank(stars: int, commits: int, expected: str):
    assert calculate_repo_rank(stars, commits) == expected
