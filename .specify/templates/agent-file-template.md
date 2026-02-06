# github-stats-card Development Context

Auto-generated from all feature plans. Last updated: [DATE]

## Active Technologies

- **Python**: 3.13+
- **Manager**: `uv`
- **CLI**: Click
- **API**: Requests (GitHub REST/GraphQL)
- **Testing**: Pytest, Pytest-Mock
- **Linting**: Ruff, Mypy

## Project Structure

```text
src/
├── cli.py               # Entry point
├── config.py            # Config Dataclasses
├── card.py              # Base SVG Logic
├── fetcher.py           # API Client
├── [stats/langs]_card.py # Card Logic
└── themes.py            # Themes
```

## Code Style

- **Formatting**: Black-compatible via `ruff format`
- **Linting**: `ruff check` (Imports, Naming, Bugbear)
- **Typing**: `mypy --strict`
- **Docstrings**: Google Style

## Recent Changes

[LAST 3 FEATURES]

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->