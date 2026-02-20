# Quickstart: Rework Ranking Calculation

**Feature**: Rework Ranking Calculation
**Version**: 1.0.0

## Overview

The `contrib` command now calculates ranks for repositories based on their popularity (stars) and your contributions.

## Usage

Generate your top contributor card:

```bash
uv run github-stats-card contrib --username [user]
```

## How It Works

1.  **Star-Based Tiers**: The base rank is determined by the repository's star count.
    *   **S**: > 10,000 Stars (e.g., Debezium)
    *   **A**: > 1,000 Stars
    *   **B**: > 100 Stars
    *   **C**: > 10 Stars
    *   **D**: > 1 Star
2.  **Contribution Modifiers**: The rank is adjusted based on your annual contribution rate.
    *   **+**: High activity (> 50 contributions/year)
    *   **-**: Low activity (< 5 contributions/year)
    *   (None): Moderate activity
3.  **Example**:
    *   Repository: `debezium/debezium` (12k stars) -> **S**
    *   Your contributions: 100 commits in 2025 -> **S+** (Rate = 100/1 = 100)
    *   Your contributions: 2 commits in 2025 -> **S-** (Rate = 2/1 = 2)

## Configuration

No new configuration flags are required. The new ranking logic is automatically applied to all `contrib` cards.
