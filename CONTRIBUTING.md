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
   github-stats-card --help
   pytest
   ```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=github_stats_card

# Run specific test file
pytest tests/test_rank.py

# Run with verbose output
pytest -v
```

### Code Formatting

We use `black` for code formatting and `ruff` for linting:

```bash
# Format code
black github_stats_card tests

# Check formatting
black --check github_stats_card tests

# Lint code
ruff check github_stats_card tests

# Auto-fix linting issues
ruff check --fix github_stats_card tests
```

### Type Checking

```bash
# Run mypy
mypy github_stats_card
```

### Manual Testing

```bash
# Test basic functionality
github-stats-card -u octocat -o test.svg

# Test with different themes
github-stats-card -u octocat -o test.svg --theme dark --show-icons
```

## Project Structure

```
github-stats-card/
├── github_stats_card/        # Main package
│   ├── __init__.py           # Package initialization
│   ├── __main__.py           # Entry point for python -m
│   ├── card.py               # Base SVG card renderer
│   ├── cli.py                # Command-line interface
│   ├── colors.py             # Color utilities
│   ├── fetcher.py            # GitHub API client
│   ├── i18n.py               # Internationalization
│   ├── icons.py              # SVG icon definitions
│   ├── rank.py               # Rank calculation
│   ├── stats_card.py         # Stats card renderer
│   ├── themes.py             # Theme definitions
│   └── utils.py              # Utility functions
├── tests/                    # Test suite
│   ├── test_colors.py
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
   github-stats-card -u octocat -o test.svg --theme my_theme
   ```

### Adding a New Icon

1. Open `github_stats_card/icons.py`
2. Find the SVG path from [Octicons](https://primer.style/octicons/)
3. Add it to the `ICONS` dictionary:

   ```python
   "my_icon": """<path fill-rule="evenodd" d="..." />""",
   ```

### Adding a New Stat

1. Update `fetcher.py` to fetch the new data from GitHub API
2. Update `i18n.py` to add the translation key
3. Update `stats_card.py` to include it in `all_stats` dictionary
4. Add tests in `tests/test_stats_card.py`

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
def calculate_rank(
    commits: int,
    prs: int,
    issues: int,
    reviews: int,
    stars: int,
    followers: int,
    all_commits: bool = False,
) -> RankResult:
    """
    Calculate user rank based on GitHub statistics.
    
    Args:
        commits: Total commit contributions
        prs: Total pull requests
        ...
        
    Returns:
        Dictionary with 'level' and 'percentile'
    """
    # Implementation
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
