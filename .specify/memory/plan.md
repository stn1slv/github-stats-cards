# Development Plan: GitHub Stats Card

## Current Status
The project is a fully functional Python CLI tool with robust support for two main card types: **GitHub Stats** and **Top Languages**. Both features are stable, tested, and support extensive customization. The architecture is modular, allowing for easy addition of new card types.

## Technical Stack
- **Language:** Python 3.13+
- **Dependency Management:** `uv`
- **CLI Framework:** `click`
- **HTTP Client:** `requests`
- **Testing:** `pytest` with `pytest-cov` and `pytest-mock`
- **Formatting/Linting:** `ruff`, `black`, `mypy`
- **Build System:** `hatchling`

## Project Structure
```
src/
├── __init__.py
├── __main__.py      # Module entry point
├── card.py          # Base SVG card renderer (shared)
├── cli.py           # Command-line interface
├── colors.py        # Color parsing and utilities
├── config.py        # Configuration dataclasses
├── constants.py     # Centralized constants
├── exceptions.py    # Custom exceptions
├── fetcher.py       # Stats Card data fetcher
├── i18n.py          # Internationalization support
├── icons.py         # SVG icons
├── langs_card.py    # Top Languages Card renderer
├── langs_fetcher.py # Top Languages data fetcher
├── rank.py          # Ranking algorithm (Stats Card)
├── stats_card.py    # Stats Card renderer
├── themes.py        # Theme definitions
└── utils.py         # General utility functions
```

## Primary Dependencies
- `requests>=2.28.0`: For GitHub API interaction.
- `click>=8.0.0`: For the command-line interface.

## Configuration
- `GITHUB_TOKEN`: Environment variable for GitHub authentication.
- `GITHUB_API_URL`: Custom REST API URL (optional).
- `GITHUB_GRAPHQL_URL`: Custom GraphQL endpoint (optional).

## Development Guidelines
- Use `uv run` for all development tasks.
- Maintain strict typing with `mypy`.
- Follow Google-style docstrings.
- Ensure 100% test coverage for core logic (rank calculation, config parsing).

## Recent Changes (Baseline)
- **Stats Card:** Full implementation including ranking, custom icons, and hiding/showing specific stats.
- **Top Languages Card:** Full implementation with 5 layouts (normal, compact, donut, donut-vertical, pie) and smart weighting logic.
- **Theming:** Support for 50+ themes and custom color overrides.
- **CI/CD:** GitHub Action integration for automated generation.

## Future Work
- **Planned: Repository Card:** Implement a third card type to display statistics for a specific repository (stars, forks, issues, language breakdown).
  - *Status:* Conceptual.
  - *Requirements:* New `repo-card` command, fetcher for repo-specific data, and renderer.
- Add more themes.
- Support more GitHub statistics (e.g., discussions, achievements).
- Improve SVG accessibility (aria-labels).
- Add support for private repositories (requires additional token scopes).
