"""Tests for color parsing and validation."""

import pytest

from src.rendering.colors import (
    is_valid_hex_color,
    is_valid_gradient,
    parse_color,
    get_card_colors,
)


@pytest.mark.parametrize(
    "color,expected",
    [
        ("ffffff", True),
        ("fff", True),
        ("ff00ff00", True),
        ("f0f0", True),
        ("gggggg", False),
        ("ff", False),
        ("fffff", False),
    ],
)
def test_is_valid_hex_color(color: str, expected: bool):
    assert is_valid_hex_color(color) is expected


@pytest.mark.parametrize(
    "parts,expected",
    [
        (["90", "ff0000", "00ff00"], True),
        (["90", "ff0000"], False),
        (["90", "gggggg", "00ff00"], False),
    ],
)
def test_is_valid_gradient(parts: list[str], expected: bool):
    assert is_valid_gradient(parts) is expected


@pytest.mark.parametrize(
    "color,fallback,expected",
    [
        ("2f80ed", "#000", "#2f80ed"),
        ("90,ff0000,00ff00", "#000", ["90", "ff0000", "00ff00"]),
        ("invalid", "#000", "#000"),
        (None, "#000", "#000"),
    ],
)
def test_parse_color(color, fallback, expected):
    assert parse_color(color, fallback) == expected


def test_get_card_colors_default():
    colors = get_card_colors()
    assert colors["title_color"] == "#2f80ed"
    assert colors["text_color"] == "#434d58"
    assert colors["bg_color"] == "#fffefe"


def test_get_card_colors_theme():
    colors = get_card_colors(theme="radical")
    assert colors["title_color"] == "#fe428e"
    assert colors["text_color"] == "#a9fef7"
    assert colors["bg_color"] == "#141321"


def test_get_card_colors_custom_overrides():
    colors = get_card_colors(title_color="ff0000", text_color="00ff00")
    assert colors["title_color"] == "#ff0000"
    assert colors["text_color"] == "#00ff00"
    # Others should be default
    assert colors["bg_color"] == "#fffefe"


def test_get_card_colors_gradient():
    colors = get_card_colors(bg_color="45,ff0000,00ff00")
    assert colors["bg_color"] == ["45", "ff0000", "00ff00"]


def test_get_card_colors_ring_color_default():
    # Should fallback to title color
    colors = get_card_colors(theme="default")
    assert colors["ring_color"] == colors["title_color"]


def test_get_card_colors_ring_color_custom():
    colors = get_card_colors(ring_color="ff0000")
    assert colors["ring_color"] == "#ff0000"
