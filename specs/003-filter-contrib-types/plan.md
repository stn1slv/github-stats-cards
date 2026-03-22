# Implementation Plan: Filter Contribution Types for Contributor Card

**Branch**: `003-filter-contrib-types` | **Date**: 2026-03-22 | **Spec**: [specs/003-filter-contrib-types/spec.md](spec.md)
**Input**: Feature specification from `/specs/003-filter-contrib-types/spec.md`

## Summary

Add an optional configuration parameter to the Contributor Card to specify exactly which types of contributions (commits, PRs, issues, code reviews) should be fetched and ranked. This will be configurable via a new CLI flag `--types` (or `--contrib-types`) and via a GitHub Actions input parameter `contrib_types`.

## Technical Context

**Language/Version**: Python 3.13+ (Managed by `uv`)
**Primary Dependencies**: Click (CLI), httpx (API), Built-in XML/SVG libraries
**Testing**: `pytest` (Unit), `pytest-mock` (API mocking)
**Linting/Formatting**: `ruff` (Lint+Format), `mypy` (Strict Typing)
**Project Structure**: `src/` layout with `tests/`
**Performance Goals**: Decrease or maintain local generation time (fetching fewer types may slightly improve GraphQL response times).
**Constraints**: Ensure safe default (default includes only `commits`). Secure token handling remains unchanged.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. CLI-First**: Does this feature expose functionality via flags/args in `src/cli.py`? Yes, adding `--types`.
- [x] **II. Local Generation**: Does it avoid external dependencies for rendering? Yes, only changes data fetching.
- [x] **III. Modern Python**: Is it typed (`mypy` strict) and `ruff` compliant? Yes, updating dataclasses.
- [x] **IV. Visuals**: Is the SVG output accessible and themeable? Yes, visual output is unaffected.
- [x] **V. Testing**: Are unit tests included? Yes, test_cli and test_fetcher will be updated.

## Project Structure

### Documentation (this feature)

```text
specs/003-filter-contrib-types/
├── plan.md              # This file
├── research.md          # Research & Design
├── data-model.md        # Data Structures & Config
├── quickstart.md        # Usage Guide
└── tasks.md             # Implementation Tasks
```

### Source Code

```text
src/
├── core/                
│   ├── config.py        # Update ContribFetchConfig
│   └── utils.py         # Update arg parsing if necessary
├── github/              
│   └── fetcher.py       # Update GraphQL query construction in _async_process_year_contributions
└── cli.py               # Add Click option for --types/--contrib-types

tests/
├── test_cli.py          # Add tests for new flag parsing
├── test_fetcher.py      # Mocked API tests for conditional queries
└── test_contrib_card.py # Integration test behavior

action.yml               # Add `contrib_types` input
```

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
