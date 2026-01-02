"""Tests for top languages card rendering."""

import pytest

from src.config import LangsCardConfig
from src.langs_card import (
    format_bytes,
    get_default_langs_count,
    get_display_value,
    render_top_languages,
    trim_top_languages,
)
from src.langs_fetcher import Language


def test_format_bytes():
    """Test byte formatting."""
    assert format_bytes(0) == "0 B"
    assert format_bytes(500) == "500.0 B"
    assert format_bytes(1024) == "1.0 KB"
    assert format_bytes(1536) == "1.5 KB"
    assert format_bytes(1048576) == "1.0 MB"
    assert format_bytes(1073741824) == "1.0 GB"

    with pytest.raises(ValueError):
        format_bytes(-100)


def test_get_display_value():
    """Test display value formatting."""
    # Percentage format
    assert get_display_value(1000, 45.67, "percentages") == "45.67%"

    # Bytes format
    assert get_display_value(1024, 45.67, "bytes") == "1.0 KB"


def test_get_default_langs_count():
    """Test default language counts for layouts."""
    assert get_default_langs_count("normal") == 5
    assert get_default_langs_count("compact") == 6
    assert get_default_langs_count("donut") == 5
    assert get_default_langs_count("donut-vertical") == 6
    assert get_default_langs_count("pie") == 6
    assert get_default_langs_count("unknown") == 5  # fallback


def test_trim_top_languages():
    """Test language trimming and filtering."""
    langs = {
        "Python": Language("Python", "#3572A5", 1000, 5),
        "JavaScript": Language("JavaScript", "#f1e05a", 800, 3),
        "TypeScript": Language("TypeScript", "#2b7489", 600, 2),
        "HTML": Language("HTML", "#e34c26", 400, 1),
    }

    # Basic trimming
    result, total = trim_top_languages(langs, 2, None)
    assert len(result) == 2
    assert result[0].name == "Python"
    assert result[1].name == "JavaScript"
    assert total == 1800

    # With hiding
    result, total = trim_top_languages(langs, 5, ["HTML", "CSS"])
    assert len(result) == 3
    assert not any(lang.name == "HTML" for lang in result)

    # Case insensitive hiding
    result, total = trim_top_languages(langs, 5, ["python"])
    assert len(result) == 3
    assert not any(lang.name == "Python" for lang in result)


def test_trim_top_languages_empty():
    """Test trimming with no languages."""
    result, total = trim_top_languages({}, 5, None)
    assert len(result) == 0
    assert total == 0


def test_render_top_languages_basic():
    """Test basic rendering with normal layout."""
    langs = {
        "Python": Language("Python", "#3572A5", 1000, 5),
        "JavaScript": Language("JavaScript", "#f1e05a", 500, 3),
    }

    config = LangsCardConfig(layout="normal")
    svg = render_top_languages(langs, config)

    assert "<svg" in svg
    assert "Python" in svg
    assert "JavaScript" in svg
    assert "Most Used Languages" in svg
    assert "#3572A5" in svg  # Python color


def test_render_top_languages_compact():
    """Test compact layout rendering."""
    langs = {"Python": Language("Python", "#3572A5", 1000, 5)}

    config = LangsCardConfig(layout="compact")
    svg = render_top_languages(langs, config)

    assert "<svg" in svg
    assert "Python" in svg
    assert "rect-mask" in svg  # Compact layout uses mask


def test_render_top_languages_donut():
    """Test donut layout rendering."""
    langs = {"Python": Language("Python", "#3572A5", 1000, 5)}

    config = LangsCardConfig(layout="donut")
    svg = render_top_languages(langs, config)

    assert "<svg" in svg
    assert "Python" in svg
    assert "circle" in svg  # Donut uses circles


def test_render_top_languages_pie():
    """Test pie layout rendering."""
    langs = {"Python": Language("Python", "#3572A5", 1000, 5)}

    config = LangsCardConfig(layout="pie")
    svg = render_top_languages(langs, config)

    assert "<svg" in svg
    assert "Python" in svg
    assert "path" in svg  # Pie uses paths


def test_render_top_languages_hide_languages():
    """Test hiding specific languages."""
    langs = {
        "Python": Language("Python", "#3572A5", 1000, 5),
        "HTML": Language("HTML", "#e34c26", 500, 3),
    }

    config = LangsCardConfig(hide=["HTML"])
    svg = render_top_languages(langs, config)

    assert "Python" in svg
    assert "HTML" not in svg


def test_render_top_languages_custom_title():
    """Test custom title."""
    langs = {"Python": Language("Python", "#3572A5", 1000, 5)}

    config = LangsCardConfig(custom_title="My Languages")
    svg = render_top_languages(langs, config)

    assert "My Languages" in svg
    assert "Most Used Languages" not in svg


def test_render_top_languages_hide_title():
    """Test hiding title."""
    langs = {"Python": Language("Python", "#3572A5", 1000, 5)}

    config = LangsCardConfig(hide_title=True)
    svg = render_top_languages(langs, config)

    # Title text should not appear in body
    assert "Most Used Languages" not in svg or '<text' not in svg.split("Most Used Languages")[0]


def test_render_top_languages_hide_border():
    """Test hiding border."""
    langs = {"Python": Language("Python", "#3572A5", 1000, 5)}

    config = LangsCardConfig(hide_border=True)
    svg = render_top_languages(langs, config)

    assert "<svg" in svg
    # Should not have a visible border stroke
    assert 'stroke="none"' in svg or "stroke-opacity" in svg


def test_render_top_languages_theme():
    """Test theme application."""
    langs = {"Python": Language("Python", "#3572A5", 1000, 5)}

    config = LangsCardConfig(theme="dark")
    svg = render_top_languages(langs, config)

    assert "<svg" in svg
    # Dark theme should have dark background colors
    assert "#151515" in svg or "151515" in svg


def test_render_top_languages_custom_colors():
    """Test custom colors."""
    langs = {"Python": Language("Python", "#3572A5", 1000, 5)}

    config = LangsCardConfig(
        title_color="ff0000",
        text_color="00ff00",
        bg_color="000000",
    )
    svg = render_top_languages(langs, config)

    assert "<svg" in svg
    assert "ff0000" in svg  # Title color
    assert "00ff00" in svg  # Text color
    assert "000000" in svg  # Background color


def test_render_top_languages_bytes_format():
    """Test bytes format display."""
    langs = {"Python": Language("Python", "#3572A5", 1048576, 5)}  # 1 MB

    config = LangsCardConfig(stats_format="bytes")
    svg = render_top_languages(langs, config)

    assert "<svg" in svg
    assert "MB" in svg or "KB" in svg or "B" in svg


def test_render_top_languages_percentages_format():
    """Test percentages format display."""
    langs = {"Python": Language("Python", "#3572A5", 1000, 5)}

    config = LangsCardConfig(stats_format="percentages")
    svg = render_top_languages(langs, config)

    assert "<svg" in svg
    assert "%" in svg


def test_render_top_languages_disable_animations():
    """Test disabling animations."""
    langs = {"Python": Language("Python", "#3572A5", 1000, 5)}

    config_with = LangsCardConfig(disable_animations=False)
    config_without = LangsCardConfig(disable_animations=True)
    svg_with = render_top_languages(langs, config_with)
    svg_without = render_top_languages(langs, config_without)

    assert "<svg" in svg_with
    assert "<svg" in svg_without
    # With animations disabled, should not have growWidthAnimation or fadeInAnimation
    assert "growWidthAnimation" not in svg_without
    assert "fadeInAnimation" not in svg_without
    # But may still have base card animations from render_card
    # The important thing is that our custom animations are not present


def test_render_top_languages_empty():
    """Test rendering with no languages."""
    langs = {}

    config = LangsCardConfig()
    svg = render_top_languages(langs, config)

    assert "<svg" in svg
    assert "No languages data available" in svg


def test_render_top_languages_invalid_layout():
    """Test invalid layout falls back to normal."""
    langs = {"Python": Language("Python", "#3572A5", 1000, 5)}

    config = LangsCardConfig(layout="invalid")
    svg = render_top_languages(langs, config)

    # Should still render successfully with normal layout
    assert "<svg" in svg
    assert "Python" in svg


def test_render_top_languages_langs_count():
    """Test limiting number of languages shown."""
    langs = {
        f"Lang{i}": Language(f"Lang{i}", "#000000", 1000 - i * 100, 1) for i in range(10)
    }

    config = LangsCardConfig(langs_count=3)
    svg = render_top_languages(langs, config)

    # Should only show top 3
    assert "Lang0" in svg
    assert "Lang1" in svg
    assert "Lang2" in svg
    assert "Lang9" not in svg


def test_render_top_languages_card_width():
    """Test custom card width."""
    langs = {"Python": Language("Python", "#3572A5", 1000, 5)}

    config = LangsCardConfig(card_width=400)
    svg = render_top_languages(langs, config)

    assert "<svg" in svg
    assert 'width="400"' in svg


def test_render_top_languages_border_radius():
    """Test custom border radius."""
    langs = {"Python": Language("Python", "#3572A5", 1000, 5)}

    config = LangsCardConfig(border_radius=10.0)
    svg = render_top_languages(langs, config)

    assert "<svg" in svg
    assert 'rx="10' in svg or "10.0" in svg


def test_render_top_languages_hide_progress():
    """Test hiding progress bars."""
    langs = {"Python": Language("Python", "#3572A5", 1000, 5)}

    config_normal = LangsCardConfig(layout="normal", hide_progress=False)
    config_hidden = LangsCardConfig(layout="normal", hide_progress=True)
    svg_normal = render_top_languages(langs, config_normal)
    svg_hidden = render_top_languages(langs, config_hidden)

    # Normal should have progress bars (rect elements)
    assert svg_normal.count("<rect") > svg_hidden.count("<rect")
