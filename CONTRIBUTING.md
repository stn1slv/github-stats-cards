# Contributing to GitHub Stats Card

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Development Setup

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Git
- GitHub account with a Personal Access Token

### Setup Instructions

1. **Fork and clone the repository**

   ```bash
   git clone https://github.com/yourusername/github-stats-card.git
   cd github-stats-card
   ```

2. **Create a virtual environment**

   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   uv pip install -e ".[dev]"
   ```

4. **Set up GitHub token**

   ```bash
   export GITHUB_TOKEN=ghp_your_token_here
   ```

5. **Verify installation**

   ```bash
   uv run github-stats-card --help
   uv run pytest
   ```

## Development Workflow

### Running Tests

This project uses `uv` for all Python execution and testing:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test file
uv run pytest tests/test_rank.py

# Run with verbose output
uv run pytest -v
```

### Code Formatting

We use `black` for code formatting and `ruff` for linting (via `uv`):

```bash
# Format code
uv run black src tests

# Check formatting
uv run black --check src tests

# Lint code
uv run ruff check src tests

# Auto-fix linting issues
uv run ruff check --fix src tests
```

### Type Checking

```bash
# Run mypy
uv run mypy src
```

### Manual Testing

```bash
# Test basic functionality
uv run github-stats-card -u octocat -o test.svg

# Test with different themes
uv run github-stats-card -u octocat -o test.svg --theme dark --show-icons
```

## Project Structure

```
github-stats-card/
├── src/                      # Main package
│   ├── __init__.py           # Package initialization
│   ├── __main__.py           # Entry point for python -m
│   ├── card.py               # Base SVG card renderer
│   ├── cli.py                # Command-line interface
│   ├── config.py             # Configuration dataclasses
│   ├── colors.py             # Color utilities
│   ├── constants.py          # Centralized constants
│   ├── exceptions.py         # Exception hierarchy
│   ├── fetcher.py            # GitHub API client (stats)
│   ├── langs_fetcher.py      # GitHub API client (languages)
│   ├── i18n.py               # Internationalization
│   ├── icons.py              # SVG icon definitions
│   ├── langs_card.py         # Top languages card renderer
│   ├── rank.py               # Rank calculation
│   ├── stats_card.py         # Stats card renderer
│   ├── themes.py             # Theme definitions
│   └── utils.py              # Utility functions
├── tests/                    # Test suite
│   ├── test_colors.py
│   ├── test_langs_card.py
│   ├── test_langs_fetcher.py
│   ├── test_rank.py
│   ├── test_stats_card.py
│   └── test_utils.py
├── .github/workflows/        # GitHub Actions
├── pyproject.toml            # Package configuration
└── README.md                 # Documentation
```

## Making Changes

### Adding a New Theme

1. Open `github_stats_card/themes.py`
2. Add your theme to the `THEMES` dictionary:

   ```python
   "my_theme": {
       "title_color": "ff6e96",
       "icon_color": "79dafa",
       "text_color": "f8f8f2",
       "bg_color": "282a36",
   },
   ```

3. Test it:

   ```bash
   uv run github-stats-card -u octocat -o test.svg --theme my_theme
   ```

### Adding a New Icon

1. Open `github_stats_card/icons.py`
2. Find the SVG path from [Octicons](https://primer.style/octicons/)
3. Add it to the `ICONS` dictionary:

   ```python
   "my_icon": """<path fill-rule="evenodd" d="..." />""",
   ```

### Adding a New Stat

1. Update `src/fetcher.py` to fetch the new data from GitHub API
2. Update `src/i18n.py` to add the translation key
3. Update `src/stats_card.py` to include it in `all_stats` dictionary
4. Add tests in `tests/test_stats_card.py`

Example:

**Step 1: Update fetcher.py**

```python
# Add to GraphQL query
query = """
query($login: String!) {
    user(login: $login) {
        # ... existing fields
        myNewStat
    }
}
"""

# Extract in fetch_user_stats function
stats["myNewStat"] = user_data.get("myNewStat", 0)
```

**Step 2: Update i18n.py**

```python
TRANSLATIONS = {
    "en": {
        # ... existing translations
        "statcard_mynewstat": "My New Stat",
    },
}
```

**Step 3: Update stats_card.py**

```python
# In render_stats_card function
all_stats = {
    # ... existing stats
    "myNewStat": {
        "label": get_translation("statcard_mynewstat", config.locale),
        "value": stats.get("myNewStat", 0),
        "icon": get_icon("star"),  # Choose appropriate icon
    },
}
```

**Step 4: Add tests**

```python
# In tests/test_stats_card.py
def test_render_with_new_stat():
    from src.config import StatsCardConfig
    from src.stats_card import render_stats_card
    
    stats = {"myNewStat": 100, "name": "Test User"}
    config = StatsCardConfig(show=["myNewStat"])
    
    svg = render_stats_card(stats, config)
    assert "My New Stat" in svg
    assert "100" in svg
```

### Adding a Translation

1. Open `github_stats_card/i18n.py`
2. Add a new locale to `TRANSLATIONS`:

   ```python
   "es": {
       "statcard_title": "Estadísticas de GitHub de {name}",
       "statcard_totalstars": "Estrellas Totales",
       # ... more translations
   },
   ```

## Submitting Changes

### Commit Guidelines

We follow conventional commits:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Examples:

```bash
git commit -m "feat: add new tokyonight theme"
git commit -m "fix: correct rank calculation for edge case"
git commit -m "docs: update installation instructions"
```

### Pull Request Process

1. **Create a branch**

   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make your changes**

   - Write code
   - Add tests
   - Update documentation

3. **Run checks**

   ```bash
   pytest
   black github_stats_card tests
   ruff check github_stats_card tests
   mypy github_stats_card
   ```

4. **Commit changes**

   ```bash
   git add .
   git commit -m "feat: add my new feature"
   ```

5. **Push to your fork**

   ```bash
   git push origin feature/my-new-feature
   ```

6. **Create Pull Request**

   - Go to GitHub
   - Click "New Pull Request"
   - Fill in the description
   - Link any related issues

### Pull Request Checklist

- [ ] Code follows the project style (black, ruff)
- [ ] All tests pass (`pytest`)
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] Commit messages follow conventions
- [ ] No breaking changes (or documented)

## Reporting Issues

### Bug Reports

Include:

- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages/stack traces

### Feature Requests

Include:

- Use case / motivation
- Proposed solution
- Alternative solutions considered
- Additional context

## Code Style

### Python

- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use docstrings for functions and classes

Example:

```python
from src.config import StatsCardConfig

def render_stats_card(stats: dict[str, Any], config: StatsCardConfig) -> str:
    """
    Render GitHub stats as an SVG card.
    
    Args:
        stats: Dictionary containing user statistics from GitHub API
        config: Configuration object with all rendering options
        
    Returns:
        SVG string representing the stats card
        
    Raises:
        RenderError: If rendering fails
    """
    # Implementation
```

### Configuration Objects

All rendering functions use configuration objects instead of individual parameters:

```python
# ✅ New API (using config objects)
from src.config import StatsCardConfig, LangsCardConfig
from src.stats_card import render_stats_card
from src.langs_card import render_top_languages

stats_config = StatsCardConfig(theme="vue-dark", show_icons=True)
svg = render_stats_card(stats, stats_config)

langs_config = LangsCardConfig(layout="compact", langs_count=8)
svg = render_top_languages(langs, langs_config)

# ❌ Old API (deprecated - do not use)
# svg = render_stats_card(stats, theme="vue-dark", show_icons=True, ...)
```

Key modules using configuration objects:
- `src/config.py` - Defines StatsCardConfig, LangsCardConfig, FetchConfig, LangsFetchConfig
- `src/stats_card.py` - render_stats_card(stats, config)
- `src/langs_card.py` - render_top_languages(langs, config)
- `src/cli.py` - Uses Config.from_cli_args() to create config objects

### Constants

Use named constants from `src/constants.py` instead of magic numbers:

```python
# ✅ Correct
from src.constants import CARD_DEFAULT_WIDTH, ANIMATION_INITIAL_DELAY_MS

width = CARD_DEFAULT_WIDTH
delay = ANIMATION_INITIAL_DELAY_MS

# ❌ Wrong
width = 495  # magic number
delay = 450  # magic number
```

### Exceptions

Use the exception hierarchy from `src/exceptions.py`:

```python
from src.exceptions import APIError, ValidationError, RenderError

# Raise specific exceptions
if not token:
    raise ValidationError("GitHub token is required")

if response.status_code != 200:
    raise APIError(f"GitHub API returned {response.status_code}")
```

### Testing

- Write tests for new features
- Maintain or improve coverage
- Use descriptive test names
- Include docstrings for complex tests

## Getting Help

- Open an issue for questions
- Join discussions in Pull Requests
- Check existing issues/PRs first

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
