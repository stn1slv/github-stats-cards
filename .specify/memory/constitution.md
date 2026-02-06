<!--
SYNC IMPACT REPORT
Version Change: 0.0.0 -> 1.0.0
Modified Principles: Initial Ratification
Added Sections: All
Removed Sections: None
Templates requiring updates: None (Templates are generic)
Follow-up TODOs: None
-->

# github-stats-card Constitution

## Core Principles

### I. CLI-First & Automation Ready
The primary interface is the Command Line. Tools must be robust, scriptable (CI/CD friendly), and fully configurable via flags and environment variables (following 12-factor app principles where applicable). Output must be pipe-friendly.

### II. Self-Contained & Local
No external service dependencies for rendering are allowed. All stats generation and SVG rendering must happen locally within the Python environment. This ensures user privacy, speed, and reliability without reliance on third-party uptime.

### III. Modern Python Standards
We strictly adhere to the modern Python ecosystem. `uv` is the mandatory package manager. Code must be typed (`mypy` strict), linted (`ruff`), formatted (`black`), and target Python 3.13+. We prefer standard library or lightweight dependencies over heavy frameworks where possible.

### IV. Visual Flexibility & Accessibility
The tool produces visual artifacts (SVGs). These must be accessible (valid markup), themeable (support for light/dark modes and user-defined colors), and internationalized (i18n support). Visual regression testing is encouraged to ensure consistency.

### V. Test-Driven Quality (NON-NEGOTIABLE)
High test coverage is mandatory. Changes must be verified via `pytest`. Critical paths (fetching, ranking, rendering) must be covered by unit tests. New features require accompanying tests before they are considered complete.

## Design Constraints

### Architecture
- **Separation of Concerns:** Distinct layers for Data Fetching (GitHub API), Data Processing (Ranking/Stats), and Presentation (SVG Rendering).
- **Configuration:** All visual and functional options must be strictly typed via Dataclasses (`StatsCardConfig`, `LangsCardConfig`).

### Security
- **Token Safety:** GitHub Tokens must be handled securely, read from environment variables or secure input, never logged or hardcoded.
- **Input Validation:** User inputs (usernames, colors, themes) must be validated before processing to prevent injection or rendering errors.

## Development Workflow

### Code Review Gates
- **Linting:** Must pass `ruff check .`
- **Formatting:** Must pass `ruff format . --check`
- **Type Checking:** Must pass `mypy .`
- **Testing:** Must pass `pytest`

### Release Process
- Semantic Versioning (MAJOR.MINOR.PATCH) is strictly followed.
- Changelog must be updated for every release.

## Governance

This constitution governs the architectural and development standards of the `github-stats-card` project.

- **Amendments:** Changes to these principles require a Pull Request with a clear rationale and must be ratified by the project maintainers.
- **Compliance:** All Pull Requests are subject to automated checks against these principles. Code violating "Modern Python Standards" or "Test-Driven Quality" will be rejected automatically by CI.
- **Runtime Guidance:** Refer to `README.md` for specific usage patterns and `CONTRIBUTING.md` for daily development tasks.

**Version**: 1.0.0 | **Ratified**: 2026-02-06 | **Last Amended**: 2026-02-06