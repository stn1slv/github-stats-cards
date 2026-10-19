"""Color parsing and validation utilities."""

import math
import re

from .themes import THEMES


def is_valid_hex_color(color: str) -> bool:
    """
    Check if string is a valid hex color code.

    Args:
        color: Color string to validate (without # prefix)

    Returns:
        True if valid hex color (3, 4, 6, or 8 digits)
    """
    pattern = r"^([A-Fa-f0-9]{8}|[A-Fa-f0-9]{6}|[A-Fa-f0-9]{3}|[A-Fa-f0-9]{4})$"
    return bool(re.match(pattern, color))


def is_valid_gradient(colors: list[str]) -> bool:
    """
    Check if colors list represents a valid gradient.

    Args:
        colors: List of color strings (first element is angle, rest are hex colors)

    Returns:
        True if valid gradient specification
    """
    return len(colors) > 2 and _is_angle(colors[0]) and all(is_valid_hex_color(c) for c in colors[1:])


def _is_angle(value: str) -> bool:
    """Check that a gradient angle is a whole number of degrees, optionally negative.

    Bounded to six digits: int() refuses strings past Python's digit limit, so an
    absurdly long angle would otherwise pass validation and crash the render.
    """
    return bool(re.fullmatch(r"-?\d{1,6}", value))


def parse_color(color: str | None, fallback: str) -> str | list[str]:
    """
    Parse color string, supporting both solid colors and gradients.

    Args:
        color: Color string (hex or gradient: "angle,color1,color2,...")
        fallback: Fallback color if parsing fails

    Returns:
        Parsed color with # prefix, or list of colors for gradient

    Examples:
        >>> parse_color("2f80ed", "#000")
        '#2f80ed'
        >>> parse_color("90,ff0000,00ff00", "#000")
        ['90', 'ff0000', '00ff00']
    """
    if not color:
        return fallback

    # Check for gradient (comma-separated)
    colors = color.split(",")
    if len(colors) > 1 and is_valid_gradient(colors):
        return colors  # Return gradient specification

    # Single color
    if is_valid_hex_color(color):
        return f"#{color}"

    return fallback


def get_card_colors(
    theme: str = "default",
    title_color: str | None = None,
    text_color: str | None = None,
    icon_color: str | None = None,
    bg_color: str | None = None,
    border_color: str | None = None,
    ring_color: str | None = None,
) -> dict[str, str | list[str]]:
    """
    Get resolved colors with theme defaults and custom overrides.

    Args:
        theme: Theme name
        title_color: Custom title color (hex without #)
        text_color: Custom text color
        icon_color: Custom icon color
        bg_color: Custom background color (or gradient)
        border_color: Custom border color
        ring_color: Custom rank ring color

    Returns:
        Dictionary with resolved colors
    """
    selected_theme = THEMES.get(theme, THEMES["default"])
    default_theme = THEMES["default"]

    return {
        "title_color": parse_color(
            title_color or selected_theme.get("title_color"),
            f"#{default_theme['title_color']}",
        ),
        "text_color": parse_color(
            text_color or selected_theme.get("text_color"),
            f"#{default_theme['text_color']}",
        ),
        "icon_color": parse_color(
            icon_color or selected_theme.get("icon_color"),
            f"#{default_theme['icon_color']}",
        ),
        "bg_color": parse_color(
            bg_color or selected_theme.get("bg_color"),
            f"#{default_theme['bg_color']}",
        ),
        "border_color": parse_color(
            border_color or selected_theme.get("border_color", default_theme["border_color"]),
            f"#{default_theme['border_color']}",
        ),
        "ring_color": parse_color(
            ring_color or selected_theme.get("ring_color") or selected_theme.get("title_color"),
            f"#{default_theme['title_color']}",
        ),
    }


def resolve_color(color: str | list[str], fallback: str = "#000000") -> str:
    """
    Collapse a parsed color to a single CSS color string.

    ``parse_color`` returns a list for a gradient spec ("angle,color1,color2").
    Only the card background can render a gradient; every other slot (title, text,
    icon, border, ring) is a single CSS color. Without this collapse the list is
    interpolated into the SVG as its Python repr, producing invalid CSS such as
    ``fill: ['90', 'ff0000', '00ff00']``.

    Args:
        color: A ``#hex`` string, or a gradient list ``[angle, color1, ...]``
        fallback: Returned when the gradient list carries no color stop

    Returns:
        A single color string with a ``#`` prefix

    Examples:
        >>> resolve_color("#2f80ed")
        '#2f80ed'
        >>> resolve_color(["90", "ff0000", "00ff00"])
        '#ff0000'
    """
    if isinstance(color, list):
        stops = color[1:]
        return f"#{stops[0]}" if stops else fallback
    return color


def format_gradient(colors: list[str]) -> tuple[str, str]:
    """
    Format gradient colors for SVG.

    Args:
        colors: List [angle, color1, color2, ...]

    Returns:
        Tuple of (gradient_id, gradient_svg_definition)
    """
    angle = colors[0]
    color_stops = colors[1:]

    # Convert the angle to a gradient vector through the card centre: 0 runs left
    # to right and 90 top to bottom. The angle is measured on the card's bounding
    # box, not on screen, so 45 always runs corner to corner whatever the card's
    # shape. The half-length grows with the angle so the end lines touch the far
    # corners, as a CSS gradient's do, instead of leaving flat-colored ends.
    angle_num = int(angle) % 360 if _is_angle(angle) else 0
    radians = math.radians(angle_num)
    cos, sin = math.cos(radians), math.sin(radians)
    half_length = 50 * (abs(cos) + abs(sin))
    dx, dy = half_length * cos, half_length * sin
    # `+ 0.0` turns a rounded -0.0 (float noise at 180 and 270) into 0.0
    x1, y1, x2, y2 = (f"{round(v, 2) + 0.0:g}%" for v in (50 - dx, 50 - dy, 50 + dx, 50 + dy))

    stops = []
    step = 100 / (len(color_stops) - 1) if len(color_stops) > 1 else 100
    for i, color in enumerate(color_stops):
        offset = i * step
        stops.append(f'<stop offset="{offset}%" stop-color="#{color}" />')

    gradient_id = "gradient"
    gradient_svg = f"""
    <linearGradient id="{gradient_id}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">
      {chr(10).join(stops)}
    </linearGradient>
    """

    return gradient_id, gradient_svg
