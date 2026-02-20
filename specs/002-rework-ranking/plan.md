# Implementation Plan: Rework Ranking Calculation

**Branch**: `002-rework-ranking` | **Date**: 2026-02-20 | **Spec**: [specs/002-rework-ranking/spec.md](specs/002-rework-ranking/spec.md)
**Input**: Feature specification from `/specs/002-rework-ranking/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.gemini/commands/speckit.plan.toml` for the execution workflow.

## Summary

The `contrib` command will calculate ranks for individual repositories based on their star count (Base Rank) and the user's contribution rate (Modifier).
- **Base Rank**: Determined by repository star count (S > 10k, A > 1k, B > 100, C > 10, D > 1).
- **Modifier**: Determined by user's average annual contributions (`+` for >50/year, `-` for <5/year).
- **Visuals**: Contributor card SVG will display specific ranks (e.g., "S", "A+") next to each repository, auto-scaling font size for 2-character ranks.
- **Legacy**: The main `stats` command logic remains unchanged.

## Technical Context

**Language/Version**: Python 3.13+ (Managed by `uv`)
**Primary Dependencies**: Click (CLI), Requests (API), Built-in XML/SVG libraries
**Testing**: `pytest` (Unit), `pytest-mock` (API mocking)
**Linting/Formatting**: `ruff` (Lint+Format), `mypy` (Strict Typing)
**Project Structure**: `src/` layout with `tests/`
**Performance Goals**: <500ms local generation time
**Constraints**: No external SVG rendering services; Secure token handling

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. CLI-First**: Does this feature expose functionality via flags/args in `src/cli.py`?
- [x] **II. Local Generation**: Does it avoid external dependencies for rendering?
- [x] **III. Modern Python**: Is it typed (`mypy` strict) and `ruff` compliant?
- [x] **IV. Visuals**: Is the SVG output accessible and themeable?
- [x] **V. Testing**: Are unit tests included?

## Project Structure

### Documentation (this feature)

```text
specs/002-rework-ranking/
├── plan.md              # This file
├── research.md          # Research & Design (Completed)
├── data-model.md        # Data Structures & Config (Completed)
├── quickstart.md        # Usage Guide (Completed)
└── tasks.md             # Implementation Tasks (To Be Created)
```

### Source Code

```text
src/
├── core/                # Shared foundational logic
│   ├── config.py        # Centralized configuration
│   ├── constants.py     # Centralized constants
│   ├── exceptions.py    # Custom exceptions
│   └── utils.py         # General utility functions
├── github/              # GitHub-specific integration
│   ├── client.py        # Centralized REST/GraphQL client
│   ├── fetcher.py       # Stats Card data fetcher (Updated: `fetch_contributor_stats`)
│   └── langs_fetcher.py # Top Languages data fetcher
│   └── rank.py          # (New: `calculate_repo_rank`)
├── rendering/           # SVG generation and visual logic
│   ├── base.py          # Base SVG card renderer (shared)
│   ├── colors.py        # Color parsing and utilities
│   ├── icons.py         # SVG icons
│   ├── langs.py         # Top Languages Card renderer
│   ├── stats.py         # Stats Card renderer
│   ├── contrib.py       # Contributor Card renderer (Updated: Visuals)
│   └── themes.py        # Theme definitions
└── cli.py               # CLI orchestration

tests/
├── test_cli.py          # Integration tests for commands
├── test_fetcher.py      # Mocked API tests (Updated)
├── test_rank.py         # Ranking logic tests (New)
└── test_contrib_rendering.py # Visual regression tests (Updated)
```

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| New Ranking Logic | Requested feature (repository-specific ranking) | Global rank reused (current) is misleading for individual repos |
| Font Scaling | Support for 2-char ranks (A+, S-) | Expanding card width would break layout consistency |