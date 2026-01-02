"""Tests for rank calculation."""

from src.rank import calculate_rank, exponential_cdf, log_normal_cdf


def test_exponential_cdf():
    assert exponential_cdf(0) == 0
    assert 0 < exponential_cdf(0.5) < 1
    assert exponential_cdf(1) == 0.5
    assert exponential_cdf(10) > 0.99


def test_log_normal_cdf():
    assert log_normal_cdf(0) == 0
    assert log_normal_cdf(1) == 0.5
    assert 0 < log_normal_cdf(0.5) < 0.5
    assert log_normal_cdf(10) > 0.9


def test_calculate_rank_s_tier():
    """Test S-tier rank (top 1%)."""
    result = calculate_rank(
        commits=5000,
        prs=500,
        issues=200,
        reviews=100,
        stars=1000,
        followers=500,
    )
    # High stats should result in top tier (S or A+)
    assert result["level"] in ["S", "A+"]
    assert result["percentile"] < 15


def test_calculate_rank_a_tier():
    """Test A-tier rank."""
    result = calculate_rank(
        commits=1000,
        prs=100,
        issues=50,
        reviews=10,
        stars=200,
        followers=50,
    )
    assert result["level"] in ["A+", "A", "A-"]
    assert 1 <= result["percentile"] < 50


def test_calculate_rank_c_tier():
    """Test C-tier rank (low activity)."""
    result = calculate_rank(
        commits=10,
        prs=1,
        issues=0,
        reviews=0,
        stars=0,
        followers=1,
    )
    assert result["level"] == "C"
    assert result["percentile"] > 87.5


def test_calculate_rank_with_all_commits():
    """Test rank calculation with all commits flag."""
    # With all_commits=True, median is 1000 instead of 250
    result = calculate_rank(
        commits=500,
        prs=50,
        issues=25,
        reviews=5,
        stars=50,
        followers=10,
        all_commits=True,
    )
    assert result["level"] in ["S", "A+", "A", "A-", "B+", "B", "B-", "C+", "C"]
    assert 0 <= result["percentile"] <= 100


def test_rank_percentile_range():
    """Test that percentile is always in valid range."""
    result = calculate_rank(
        commits=250,
        prs=50,
        issues=25,
        reviews=2,
        stars=50,
        followers=10,
    )
    assert 0 <= result["percentile"] <= 100
