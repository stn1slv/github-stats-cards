# GitHub Copilot Instructions for GitHub Stats Card

## Project Overview

This is a Python CLI tool that generates beautiful GitHub stats cards as SVG images. The tool fetches GitHub statistics via the GitHub GraphQL API and renders them as customizable SVG cards with 50+ built-in themes.

**Key Purpose**: Generate standalone SVG files showing GitHub user statistics (stars, commits, PRs, issues, etc.) that can be embedded in README files.

## Technology Stack

- **Language**: Python 3.13+
- **Package Manager**: `uv` (Astral's fast Python package installer and resolver)
- **CLI Framework**: Click
- **HTTP Client**: httpx (async-capable)
- **Testing**: pytest with pytest-cov
- **Code Quality**: black (formatting), ruff (linting), mypy (type checking)
- **Build System**: setuptools via pyproject.toml

## Development Workflow

### Always Use `uv` for Execution

**IMPORTANT**: This project uses `uv` for ALL Python execution, testing, and package management. Never suggest plain `python` or `pytest` commands.

✅ Correct:
```bash
uv run pytest
uv run github-stats-card -u username -o output.svg
uv run black src tests
uv run mypy src
```

❌ Incorrect:
```bash
python -m pytest
pytest
github-stats-card -u username -o output.svg
black src tests
```

### Testing Commands
- Run all tests: `uv run pytest`
- Run with coverage: `uv run pytest --cov=src`
- Run specific file: `uv run pytest tests/test_rank.py`
- Verbose output: `uv run pytest -v`

### Code Quality Commands
- Format code: `uv run black src tests`
- Check formatting: `uv run black --check src tests`
- Lint: `uv run ruff check src tests`
- Auto-fix linting: `uv run ruff check --fix src tests`
- Type check: `uv run mypy src`

## Project Structure

```
src/
├── __init__.py          # Package initialization, version info
├── __main__.py          # Entry point for `python -m github_stats_card`
├── card.py              # Base SVG card rendering class
├── cli.py               # Click-based CLI interface with all options
├── colors.py            # Color parsing, validation, gradient handling
├── fetcher.py           # GitHub GraphQL API client
├── i18n.py              # Internationalization/translations
├── icons.py             # SVG icon definitions (Octicons)
├── rank.py              # User rank calculation algorithm
├── stats_card.py        # Main stats card renderer (extends Card)
├── themes.py            # 50+ theme definitions
└── utils.py             # Utility functions (animation, formatting)

tests/
├── test_colors.py       # Color parsing and gradient tests
├── test_rank.py         # Rank calculation tests
├── test_stats_card.py   # Stats card rendering tests
└── test_utils.py        # Utility function tests
```

## Architecture Patterns

### 1. Card Rendering (card.py)
- `Card` class: Base class for all SVG card types
- Handles SVG structure, dimensions, backgrounds
- Supports gradients, borders, animations
- Methods: `render()`, `_create_gradient()`, `_create_background()`

### 2. Stats Card (stats_card.py)
- `StatsCard` extends `Card`
- Renders individual stat items with icons
- Manages layout: title, stats grid, progress bars
- Key method: `render(stats, config)` → returns SVG string

### 3. Data Fetching (fetcher.py)
- `GitHubFetcher` class: GraphQL API client
- Async-capable with httpx
- Methods: `fetch_stats()`, `_run_query()`
- Handles rate limiting and errors
- Returns dict with all stats

### 4. Theming (themes.py)
- `THEMES` dict: 50+ pre-defined themes
- Each theme has: `title_color`, `icon_color`, `text_color`, `bg_color`
- `get_theme()` function validates and returns theme config

### 5. Color Handling (colors.py)
- Validates hex colors (with/without #)
- Parses gradient syntax: `angle,color1,color2,...`
- `parse_color()`: validates single color
- `parse_gradient()`: handles gradient strings

## Coding Conventions

### Type Hints
Always use type hints for function parameters and return values:
```python
def calculate_rank(stats: dict[str, int]) -> str:
    """Calculate user rank based on stats."""
    total_score: int = 0
    # ...
    return rank
```

### Docstrings
Use Google-style docstrings for all public functions/classes:
```python
def fetch_stats(username: str, token: str) -> dict[str, Any]:
    """Fetch GitHub statistics for a user.
    
    Args:
        username: GitHub username to fetch stats for
        token: GitHub Personal Access Token
        
    Returns:
        Dictionary containing user statistics
        
    Raises:
        ValueError: If username is invalid
        RuntimeError: If API request fails
    """
```

### Error Handling
- Use `click.ClickException` for CLI errors
- Use specific exception types (ValueError, RuntimeError, etc.)
- Always provide helpful error messages
```python
if not token:
    raise click.ClickException("GitHub token required. Set GITHUB_TOKEN or use --token")
```

### Constants
- Use UPPER_CASE for constants
- Define at module level
```python
DEFAULT_WIDTH = 495
DEFAULT_HEIGHT = 195
CARD_PADDING = 25
```

### Configuration
- Use dicts for config objects
- Prefer explicit keys over kwargs
```python
config = {
    "hide_border": False,
    "show_icons": True,
    "locale": "en",
    "theme": "default"
}
```

## Testing Patterns

### Test Structure
```python
import pytest
from src.module import function

def test_function_basic_case():
    """Test basic functionality."""
    result = function(input_data)
    assert result == expected

def test_function_edge_case():
    """Test edge case handling."""
    with pytest.raises(ValueError):
        function(invalid_input)
```

### Fixtures
Use fixtures for repeated setup:
```python
@pytest.fixture
def sample_stats():
    return {
        "totalStars": 1000,
        "totalCommits": 500,
        "totalPRs": 50,
    }
```

### Parametrize
Use parametrize for multiple test cases:
```python
@pytest.mark.parametrize("color,expected", [
    ("ff0000", "ff0000"),
    ("#ff0000", "ff0000"),
    ("red", ValueError),
])
def test_parse_color(color, expected):
    # test implementation
```

## Common Tasks

### Adding a New Theme
1. Add to `src/themes.py` THEMES dict
2. Test with: `uv run github-stats-card -u octocat -o test.svg --theme new_theme`
3. Document in EXAMPLES.md

### Adding a New Stat
1. Update `src/fetcher.py` GraphQL query
2. Add to `src/stats_card.py` all_stats dict
3. Add translation in `src/i18n.py`
4. Add test in `tests/test_stats_card.py`

### Adding a New Icon
1. Get SVG path from [Octicons](https://primer.style/octicons/)
2. Add to `src/icons.py` ICONS dict
3. Use in stats_card.py via `get_icon()`

### Adding a Translation
1. Add locale to `src/i18n.py` TRANSLATIONS dict
2. Include all keys from "en" locale
3. Test with `--locale` option

## GraphQL API Patterns

The project uses GitHub's GraphQL API v4:
```python
query = """
query($login: String!) {
    user(login: $login) {
        name
        contributionsCollection {
            totalCommitContributions
        }
    }
}
"""
variables = {"login": username}
```

Key queries:
- User stats: contributions, repositories, issues, PRs
- Repository data: stargazers, forks
- Commit history: commit counts per year

## SVG Generation Patterns

### Basic SVG Structure
```python
svg = f"""
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <defs>{gradients}</defs>
    <rect width="{width}" height="{height}" fill="url(#bg-gradient)"/>
    {content}
</svg>
"""
```

### CSS Animations
Use `utils.py` animations:
```python
from src.utils import create_animation
animation = create_animation()
# Add to <style> in SVG
```

## CLI Option Patterns

When adding new CLI options:
```python
@click.option(
    "--new-option",
    type=str,
    default="default_value",
    help="Description of what this option does"
)
```

Follow existing patterns in `src/cli.py`:
- Use long names with dashes: `--hide-border`
- Provide defaults
- Add comprehensive help text
- Group related options together

## File Naming and Imports

### Import Order
1. Standard library
2. Third-party packages
3. Local modules

```python
import sys
from typing import Any, Optional

import click
import httpx

from src.colors import parse_color
from src.themes import get_theme
```

### Module Organization
- One class per file for major components
- Group related utilities in utils.py
- Keep tests parallel to source structure

## Performance Considerations

- Use async/await for API calls (httpx)
- Cache theme lookups
- Minimize SVG string concatenation (use f-strings or join)
- Avoid unnecessary GraphQL queries

## Security Best Practices

- Never log or print GitHub tokens
- Validate all user inputs
- Sanitize strings used in SVG output (prevent XSS)
- Use environment variables for sensitive data

## Documentation Standards

- Update README.md for user-facing features
- Update EXAMPLES.md with new use cases
- Update CONTRIBUTING.md for development changes
- Keep QUICKSTART.md focused on getting started
- All code changes should include tests

## Git Commit Messages

Follow conventional commits:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation only
- `test:` - Test additions/changes
- `refactor:` - Code restructuring
- `chore:` - Maintenance tasks

Examples:
```
feat: add tokyonight theme
fix: correct rank calculation for users with 0 commits
docs: update installation instructions for uv
test: add tests for gradient parsing
```

## Dependencies Management

Always update pyproject.toml when adding dependencies:
```toml
[project]
dependencies = [
    "click>=8.0",
    "httpx>=0.24",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black>=23.0",
]
```

Then install with: `uv pip install -e ".[dev]"`

## Common Patterns to Follow

### Click Commands
```python
@click.command()
@click.option("-u", "--username", required=True, help="GitHub username")
def main(username: str) -> None:
    """Generate GitHub stats card."""
    try:
        # implementation
    except Exception as e:
        raise click.ClickException(str(e))
```

### Configuration Validation
```python
def validate_config(config: dict[str, Any]) -> None:
    """Validate configuration options."""
    if config.get("hide_border") and config.get("border_radius"):
        raise ValueError("Cannot specify border_radius when hide_border is True")
```

### SVG Component Building
```python
def render_stat_item(stat_name: str, value: str, icon: str, y: int) -> str:
    """Render a single stat item."""
    return f"""
    <g transform="translate(0, {y})">
        {icon}
        <text x="30" y="15">{stat_name}:</text>
        <text x="200" y="15">{value}</text>
    </g>
    """
```

## Remember

1. **Always use `uv run` for any Python execution**
2. **Type hints are mandatory for all functions**
3. **Tests are required for all new features**
4. **Follow existing code structure and patterns**
5. **Update relevant documentation files**
6. **Keep SVG generation efficient and readable**
7. **Validate all inputs before processing**
8. **Use descriptive variable names**
9. **Follow conventional commit messages**
10. **Keep functions focused and single-purpose**
