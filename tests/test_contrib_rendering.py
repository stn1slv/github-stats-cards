"""Tests for contributor card rendering logic."""

import base64
import re

from src.core.config import ContribCardConfig
from src.core.constants import FONT_SIZE_STAT
from src.core.utils import measure_text
from src.rendering.contrib import render_contrib_card


def test_render_contrib_card_repo_name_only():
    """Test that the card renders only the repository name, not the owner."""
    stats = {
        "repos": [
            {
                "name": "facebook/react",
                "stars": 200000,
                "commits": 10,
                "prs": 5,
                "issues": 2,
                "reviews": 1,
                "rank_level": "S",
                "avatar_b64": "base64data",
            }
        ]
    }
    config = ContribCardConfig()

    svg = render_contrib_card(stats, config)

    assert ">react<" in svg
    assert ">facebook/react<" not in svg


def test_render_contrib_card_rank_display():
    """Test that the card renders rank level instead of star count or row index."""
    stats = {
        "repos": [
            {
                "name": "owner/repo1",
                "stars": 100,
                "commits": 10,
                "prs": 5,
                "issues": 2,
                "reviews": 1,
                "rank_level": "A",
                "avatar_b64": None,
            },
            {
                "name": "owner/repo2",
                "stars": 50,
                "commits": 5,
                "prs": 2,
                "issues": 1,
                "reviews": 0,
                "rank_level": "B",
                "avatar_b64": None,
            },
        ]
    }
    config = ContribCardConfig()

    svg = render_contrib_card(stats, config)

    assert ">A</text>" in svg
    assert ">B</text>" in svg
    # Ranks are single characters, so the badge size is a fixed literal in the
    # template. Pin it: nothing else asserts it since the scaling was removed.
    assert 'style="font-size: 10px;">A</text>' in svg
    # The star counts should NOT be present as text
    assert ">100<" not in svg
    assert ">50<" not in svg
    # Row indices #1, #2 should NOT be present
    assert ">#1<" not in svg
    assert ">#2<" not in svg


def test_render_contrib_card_clamps_a_too_narrow_width():
    """Below the minimum the rank badge would land on top of the avatar and name."""
    stats = {
        "repos": [
            {
                "name": "facebook/react",
                "stars": 200000,
                "commits": 5,
                "prs": 2,
                "issues": 0,
                "reviews": 0,
                "rank_level": "S",
                "avatar_b64": None,
            }
        ]
    }
    svg = render_contrib_card(stats, ContribCardConfig(card_width=100))

    assert '<svg width="280"' in svg
    # Badge is right of the repo name (x=30), so the row no longer overlaps
    assert 'transform="translate(205, 7.5)"' in svg


def _single_repo_stats(name: str, avatar_b64: str | None = None) -> dict:
    return {
        "repos": [
            {
                "name": name,
                "stars": 50,
                "commits": 1,
                "prs": 0,
                "issues": 0,
                "reviews": 0,
                "rank_level": "C",
                "avatar_b64": avatar_b64,
            }
        ]
    }


def test_render_contrib_card_shortens_a_name_that_would_reach_the_rank_badge():
    """Long names used to run underneath the rank badge."""
    long_name = "a-very-long-repository-name-that-keeps-going-and-going"
    svg = render_contrib_card(_single_repo_stats(f"owner/{long_name}"), ContribCardConfig())

    shown = re.search(r'<text x="30" y="22" class="stat bold">([^<]+)</text>', svg).group(1)
    assert shown.endswith("…")
    assert long_name.startswith(shown[:-1])
    # Text starts at x=30 in the row; the badge's left edge is at card_width - 77
    assert 30 + measure_text(shown, FONT_SIZE_STAT) <= ContribCardConfig().card_width - 77


def test_render_contrib_card_keeps_a_short_name_intact():
    svg = render_contrib_card(_single_repo_stats("owner/react"), ContribCardConfig())

    assert ">react<" in svg
    assert "…" not in svg


def test_render_contrib_card_labels_a_jpeg_avatar_as_jpeg():
    """GitHub serves uploaded avatars as JPEG; they used to be labelled PNG."""
    jpeg_b64 = base64.b64encode(b"\xff\xd8\xff\xe0fake-jpeg").decode()
    png_b64 = base64.b64encode(b"\x89PNG\r\n\x1a\nfake-png").decode()

    assert f"data:image/jpeg;base64,{jpeg_b64}" in render_contrib_card(
        _single_repo_stats("o/r", jpeg_b64), ContribCardConfig()
    )
    assert f"data:image/png;base64,{png_b64}" in render_contrib_card(
        _single_repo_stats("o/r", png_b64), ContribCardConfig()
    )
