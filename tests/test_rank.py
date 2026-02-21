"""Tests for rank calculation algorithm."""

from src.github.rank import (
    calculate_user_rank,
    calculate_repo_rank,
    exponential_cdf,
    log_normal_cdf,
)


def test_exponential_cdf():
    assert exponential_cdf(0) == 0
    assert exponential_cdf(1) == 0.5
    assert exponential_cdf(2) == 0.75


def test_log_normal_cdf():
    assert log_normal_cdf(0) == 0
    assert log_normal_cdf(1) == 0.5
    assert log_normal_cdf(9) == 0.9


def test_calculate_user_rank_s_tier():
    # Extremely high stats to ensure S tier (percentile <= 1.0)
    # Using 100k for most stats to ensure CDF approaches 1.0
    result = calculate_user_rank(100000, 10000, 10000, 10000, 100000, 10000)
    assert result["level"] == "S"
    assert result["percentile"] <= 1.0


def test_calculate_user_rank_a_tier():
    # Good stats
    result = calculate_user_rank(1000, 100, 50, 20, 100, 50)
    assert result["level"] in ["S", "A+", "A"]


def test_calculate_user_rank_c_tier():
    # Low stats
    result = calculate_user_rank(10, 1, 1, 0, 0, 0)
    assert result["level"] in ["C+", "C"]


def test_calculate_user_rank_with_all_commits():
    # Same stats, but one is all-time commits (median is higher)
    res1 = calculate_user_rank(1000, 50, 25, 2, 50, 10, all_commits=False)
    res2 = calculate_user_rank(1000, 50, 25, 2, 50, 10, all_commits=True)

    # res2 should have a higher (worse) percentile because 1000 commits
    # is less impressive when compared to all-time median (1000)
    # than when compared to current year median (250)
    assert res2["percentile"] > res1["percentile"]


def test_user_rank_percentile_range():
    # Test extreme cases
    res_best = calculate_user_rank(1000000, 100000, 100000, 10000, 100000, 100000)
    res_worst = calculate_user_rank(0, 0, 0, 0, 0, 0)

    assert 0 <= res_best["percentile"] <= 100
    assert 0 <= res_worst["percentile"] <= 100
    assert res_best["percentile"] < res_worst["percentile"]


def test_calculate_repo_rank():
    # S tier (>10000 stars)
    # > 5000 commits -> "+"
    assert calculate_repo_rank(10001, 5001) == "S+"
    # 1000 commits (neutral) -> ""
    assert calculate_repo_rank(10001, 1000) == "S"
    # 50 commits (1-99 range) -> "-"
    assert calculate_repo_rank(10001, 50) == "S-"

    # Boundary: 10000 stars (Should be A, as tier is >10000)
    assert calculate_repo_rank(10000, 6000) == "A+"

    # A tier (>1000 stars)
    assert calculate_repo_rank(1001, 6000) == "A+"
    assert calculate_repo_rank(1001, 200) == "A"
    assert calculate_repo_rank(1001, 10) == "A-"

    # Boundary: 1000 stars (Should be B)
    assert calculate_repo_rank(1000, 6000) == "B+"

    # B tier (>100 stars)
    assert calculate_repo_rank(101, 6000) == "B+"

    # Boundary: 100 stars (Should be C)
    assert calculate_repo_rank(100, 6000) == "C+"

    # C tier (>10 stars)
    assert calculate_repo_rank(11, 6000) == "C+"

    # Boundary: 10 stars (Should be D)
    assert calculate_repo_rank(10, 6000) == "D+"

    # D tier (0-10 stars)
    assert calculate_repo_rank(1, 6000) == "D+"
    assert calculate_repo_rank(0, 6000) == "D+"

    # Commit Modifier Boundaries
    # 5000 commits is the upper neutral boundary (no modifier, "+" starts at > 5000)
    assert calculate_repo_rank(10001, 5000) == "S"
    # 100 commits is the lower neutral boundary (no modifier, "-" starts at < 100)
    assert calculate_repo_rank(10001, 100) == "S"

    # Edge cases
    # 0 commits: Unknown magnitude, treat as neutral (no modifier)
    assert calculate_repo_rank(10001, 0) == "S"
